# coding:utf-8
"""
    :module: dynMotion.py
    :description: Add procedural secondary / follow-through motion to Maya transforms
    :author: Michel 'Mitch' Pecqueur
    :date: 2021.11, Reworked version 2026.06

# Minimal – works on current selection, current playback range
import aresTools.dynMotion as dm
adm.dyn_motion()

# Explicit
import aresTools.dynMotion as dm
adm.dyn_motion(conserve=1.0, stiffness=0.4, damping=0.6, dyn_scl=.15
    comp=None, prm_random=(0.1, 0.1, 0.05), seed=1,
    trs=(0, 1, 0), time_shift=0,
    fromsel=True, time_range=None,
    bakeroll=True, resample=1, simplify=False)
"""

import math
import random

import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import maya.cmds as mc
from PySide6.QtWidgets import QProgressBar


def dyn_motion(objlist: list[str] = (), fromsel: bool = True,

               trs: list[int] = (0, 1, 0),
               comp: str | None = None,

               conserve: float = 1.0, stiffness: float = 0.4, damping: float = 0.6, dyn_scl: float = .15,
               prm_random: tuple[float, float, float] = (0, 0, 0), seed: int = 1,

               time_range: tuple[int, int] | None = None,
               bakeroll: bool = True, preroll: int = 0, set_infinity: bool = True,
               time_shift: int = 0,

               resample: int | None = None,
               simplify: bool = False,
               progress: QProgressBar | None = None) -> bool:
    """
    Add secondary / follow-through motion to the given transforms

    The algorithm works in 3 passes per object:
      1 re-bake – sample the original world-space motion and re-bake it
         as local keys (preserves the source animation for objects that rely on
         live constraints or rivet setups)
      2 Dynamics – run a simple spring simulation over the baked keys to
         produce lagging / oscillating motion
      3 Post-filter – optionally resample and / or simplify the resulting
         curves

    :param objlist:
        Transforms to process, Ignored when fromsel is True
    :param fromsel:
        When True (default) objlist is ignored and the current Maya selection is used instead

    :param trs:
        Enable / disable simulation for Translation, Rotation, Scale
        Each element is treated as a boolean (0 or 1)
    :param comp:
        Optional transform whose world matrix is used to compensate the
        simulation (typically parent space reference)

    :param conserve:
        Overall softening (0–1)
        Simulates atmospheric drag / viscosity
        1 = no drag (full velocity conserved)
    :param stiffness:
        Spring stiffness (0–1)
        How strongly the simulated position is pulled back toward the goal each frame
        1 = rigid (no lag)
    :param damping:
        Spring damping (0–1)
        Suppresses oscillation
        0 = no damping (bouncy forever)
    :param dyn_scl:
        Overall dynamic scale factor

    :param prm_random :
        Per-parameter randomization range applied to (conserve, stiffness, damping)
        Adds subtle asymmetry to symmetrical rigs
    :param seed:
        Random seed used for prm_random

    :param time_range:
        (start, end) frame range
        None uses the current playback range

    :param bakeroll:
        When True the timeline is advanced frame-by-frame before sampling
        Slower but required for objects evaluated via live connections (pinned controls)
        Default True
    :param preroll:
        Number of frames to simulate before first frame
    :param set_infinity:
        Set pre- and post-infinity to linear, helps with motion blur for first and last frames

    :param time_shift:
        Shift the written keyframes by this many frames relative to the simulation frame
        Useful for creating a deliberate time-offset look

    :param resample:
        If set, runs a Gaussian resample filter with this period on the output curves
        Useful for smoothing high-frequency noise
    :param simplify:
        When True, runs Maya's curve-simplify filter on the output curves
    :param progress:
        Optional progress bar for UI

    :return: True on success
    """
    if fromsel:
        objlist = mc.ls(sl=True)

    if not objlist:
        mc.warning('[dyn_motion] Nothing to process')
        return False

    # --- Time range ---
    if time_range is None:
        mn = int(mc.playbackOptions(q=True, min=True))
        mx = int(mc.playbackOptions(q=True, max=True))
    else:
        mn, mx = time_range

    fps = float(get_fps())

    objlist = hierarchical_sort(objlist, fromsel=False)

    # Initial curve filter to remove redundant keys / normalise tangents
    mc.filterCurve(objlist)

    if progress is not None:
        progress.setFormat('Simulation in progress.')

    # tuvs: expand trs to the four simulation channels
    #   0 : translation,
    #   1 : primary axis vector,
    #   2 : secondary axis vector
    #   3 : scale
    tuvs = (trs[0], trs[1], trs[1], trs[2])

    # - Per-object axis settings -
    axis_dict = {}
    for obj in objlist:
        point = True
        pa = get_primary_axis(obj)
        if pa is None:
            pa = 'x'
            point = False
        sa = secondary_axis(pa)
        order = get_axes_order(pa, sa)
        re_order = [order.index(a) for a in 'xyz'] + [3]
        ro = mc.getAttr(obj + '.ro')
        has_jo = mc.objExists(obj + '.jo')

        axis_dict[obj] = {'pa': pa, 'sa': sa, 'point': point, 're_order': re_order, 'ro': ro, 'has_jo': has_jo}

    if progress is not None:
        progress.setFormat('Simulation in progress..')

    # - Pre-compute parent matrices (avoid repeated listRelatives calls) -
    par_dict = {}
    for obj in objlist:
        parent = mc.listRelatives(obj, p=True, pa=True)
        par_dict[obj] = parent[0] if parent else None

    if progress is not None:
        progress.setFormat('Simulation in progress...')

    # -  Per-object parameter randomisation -
    if not prm_random:
        prm_random = (0, 0, 0)
    prm_dict = {}
    random.seed(seed)
    for obj in objlist:
        prm_dict[obj] = {}
        for prm, prm_value, r in zip(['conserve', 'stiffness', 'damping'], [conserve, stiffness, damping], prm_random):
            prm_dict[obj][prm] = clamp(1e-3, 1, prm_value + r * random.uniform(-1, 1))

    count = len(objlist)

    # Pass 1 – Pre-bake
    # Capture world-space motion and re-express as local keys so that the
    # dynamics pass works on clean, constraint-free curves
    if progress is not None:
        progress.setFormat('Pre-bake %p%')

    for o, obj in enumerate(objlist):
        an_data = get_animdata(obj, st=mn - preroll, ed=mx)
        bake_from_data(obj, data=an_data, trs=trs, progress=None)
        if progress is not None:
            progress.setValue((o + 1) * count // 100)

    # Pass 2 – Dynamics
    saved_time = oma.MAnimControl.currentTime()

    for o, obj in enumerate(objlist):
        if progress is not None:
            progress.setFormat(f'{shorten(obj)}: Simulation %p%')

        pa = axis_dict[obj]['pa']
        sa = axis_dict[obj]['sa']
        point = axis_dict[obj]['point']
        re_order = axis_dict[obj]['re_order']
        ro = axis_dict[obj]['ro']

        has_jo = axis_dict[obj]['has_jo']
        or_at = (['ra'], ['jo', 'ra'])[has_jo]  # Remove joint orient from matrix if transform is a joint

        cns = prm_dict[obj]['conserve']
        stf = prm_dict[obj]['stiffness']
        dmp = prm_dict[obj]['damping']

        # Spring state: current and previous simulated positions
        pos = {}  # simulated position current frame
        pos0 = {}  # simulated position previous frame

        # Accumulated output: list of per-channel values, one entry per frame
        result = []

        framecount = mx - (mn - preroll) + 1

        prev = None  # Progress bar throttling

        for f, frame in enumerate(range(mn - preroll, mx + 1)):
            if bakeroll:
                oma.MAnimControl.setCurrentTime(om.MTime(frame))
                kwarg = {}
            else:
                kwarg = {'t': frame}

            # - Build compensation and parent matrices -
            if comp:
                comp_wm = om.MMatrix(mc.getAttr(comp + '.wm', **kwarg))
            else:
                comp_wm = om.MMatrix()  # identity

            parent_name = par_dict[obj]
            if parent_name:
                pm = om.MMatrix(mc.getAttr(parent_name + '.wm', **kwarg))
            else:
                pm = om.MMatrix()  # identity

            wm = om.MMatrix(mc.getAttr(obj + '.wm', **kwarg))

            wm = scl_mat(wm, dyn_scl)
            comp_wm = scl_mat(comp_wm, dyn_scl)
            comp_wim = comp_wm.inverse()
            pm = scl_mat(pm, dyn_scl)
            pim = pm.inverse()

            if comp:
                wm = wm * comp_wim

            tm = om.MTransformationMatrix(wm)
            tr = om.MPoint(0, 0, 0) * wm
            u = axis_to_vector(pa, point) * wm  # Primary axis has to be affected by translation
            v = axis_to_vector(sa, point=False) * wm  # Secondary axis should not be affected by translation
            scl = om.MVector(tm.scale(om.MSpace.kWorld))

            goals = [tr, u, v, scl]

            values = []

            i: int
            for i, goal in enumerate(goals):
                if not tuvs[i]:
                    values.append(None)
                    continue

                # Initialise spring state on the first frame
                if frame == mn - preroll:
                    pos[i] = goal
                    pos0[i] = goal

                # Spring integration (verlet-like)
                velocity = (1. - dmp) * (pos[i] - pos0[i])
                newpos = pos[i] + velocity
                goalforce = stf * (goal - newpos)
                newpos += goalforce
                newpos = pos[i] + cns * (newpos - pos[i])

                # Express result in the appropriate local space
                if isinstance(newpos, om.MPoint):
                    if i == 1:  # Primary axis
                        res = om.MVector(om.MPoint(newpos) - om.MPoint(tr)) * comp_wm * pim
                    else:
                        res = om.MVector(om.MPoint(newpos) * comp_wm * pim)
                elif isinstance(newpos, om.MVector):
                    res = om.MVector(newpos) * comp_wm * pim
                else:
                    res = newpos

                values.append(res)

                # Advance spring state
                pos0[i] = pos[i]
                pos[i] = newpos

            result.append(values)

            # Refresh anim-curve evaluation (needed for some rivet setups)
            for ac in (mc.listConnections(obj, s=True, d=False, t='animCurve') or []):
                mc.setAttr(ac + '.nds', 2)
                mc.setAttr(ac + '.nds', 0)

            if progress is not None:
                value = (o * framecount + f + 1) * 100 // (count * framecount)
                if value != prev:
                    progress.setValue(value)
                    prev = value

        # Pass 3 – Write keys
        # Remove existing keys in the range before writing new ones
        for en, chn in zip(trs, 'trs'):
            if en:
                mc.cutKey(obj, at=[chn + a for a in 'xyz'], clear=True, time=(float(mn - preroll), float(mx + 1)))

        for t, values in zip(list(range(mn, mx + 1)), result[preroll:]):
            tt = ('auto', 'spline')[t == mn or t == mx]

            if trs[0]:
                for val, a in zip(values[0], 'xyz'):
                    chn = f'{obj}.t{a}'
                    mc.setKeyframe(chn, t=t + time_shift, v=val / dyn_scl, itt=tt, ott=tt)
                    if set_infinity:
                        acs = mc.keyframe(chn, q=True, name=True)
                        for ac in acs:
                            mc.setAttr(ac + '.pre', 1)
                            mc.setAttr(ac + '.pst', 1)

            if trs[1]:
                u, v = values[1], values[2]
                sign = (1, -1)['-' in pa]  # Flip axis depending on transform's orientation
                rm = create_matrix(u * sign, v * sign, [0, 0, 0])
                rm = reorder_matrix_rows(rm, order=re_order)

                # Remove orientation (jointOrient, rotateAxis) to set proper local rotation
                for attr in or_at:
                    er = [math.radians(a) for a in mc.getAttr(f'{obj}.{attr}', t=t)[0]]
                    r_im = om.MEulerRotation(*er).asMatrix().inverse()
                    rm *= r_im

                rot = om.MTransformationMatrix(rm).rotation().reorder(ro)
                er = [math.degrees(value) for value in rot]

                for val, a in zip(er, 'xyz'):
                    chn = f'{obj}.r{a}'
                    mc.setKeyframe(chn, t=t + time_shift, v=val, itt=tt, ott=tt)
                    if set_infinity:
                        acs = mc.keyframe(chn, q=True, name=True)
                        for ac in acs:
                            mc.setAttr(ac + '.pre', 1)
                            mc.setAttr(ac + '.pst', 1)

            if trs[2]:
                for val, a in zip(values[3], 'xyz'):
                    chn = f'{obj}.s{a}'
                    mc.setKeyframe(chn, t=t + time_shift, v=val, itt=tt, ott=tt)
                    if set_infinity:
                        acs = mc.keyframe(chn, q=True, name=True)
                        for ac in acs:
                            mc.setAttr(ac + '.pre', 1)
                            mc.setAttr(ac + '.pst', 1)

        if progress is not None:
            progress.setValue((o + 1) * 100 // count)

    # Euler filter
    mc.filterCurve(objlist)
    # Resample / simplify animation curves
    if resample:
        mc.filterCurve(objlist, f='resample', ker='gaussian2', per=resample)
    if simplify:
        mc.filterCurve(objlist, f='simplify', timeTolerance=1.0 / fps)

    oma.MAnimControl.setCurrentTime(saved_time)
    mc.ogs(r=True)
    return True


# Pre-bake helpers

def get_animdata(obj: str, st: int, ed: int) -> dict[int, list]:
    """
    Sample the local matrix of obj for every frame in [st, ed]

    :param obj:
    :param st: Start frame
    :param ed: End frame

    :return: Frame as key : Raw matrix as value (as returned by mc.getAttr)
    """
    result = {}

    has_jo = mc.objExists(obj + '.jo')  # Remove joint orient from matrix if transform is a joint
    or_at = (['ra'], ['jo', 'ra'])[has_jo]

    for frame in range(st, ed + 1):
        m = om.MMatrix(mc.getAttr(obj + '.m', t=frame))

        for attr in or_at:
            er = [math.radians(a) for a in mc.getAttr(f'{obj}.{attr}', t=frame)[0]]
            r_im = om.MEulerRotation(*er).asMatrix().inverse()
            m *= r_im

        result[frame] = m
    return result


def bake_from_data(obj: str, data: dict[int, list], trs: list[int] = (1, 1, 0),
                   progress: QProgressBar | None = None) -> bool:
    """
    Write local-transform keyframes onto obj from a sampled matrix dict

    :param obj : Given object
    :param data : As returned by get_animdata
    :param trs : Which channels to bake: Translation, Rotation, Scale
    :param progress: Optional QProgressBar

    """
    ro = mc.getAttr(obj + '.ro')  # rotation order
    count = len(data.items())
    for frame, raw_m in data.items():
        m = om.MMatrix(raw_m)
        tm = om.MTransformationMatrix(m)
        tr = om.MVector(om.MPoint(0, 0, 0) * m)
        er = tm.rotation().reorder(ro)
        er = [math.degrees(v) for v in er]
        scl = tm.scale(om.MSpace.kWorld)
        for i, a in enumerate('xyz'):
            if trs[0]:
                mc.setKeyframe(f'{obj}.t{a}', t=frame, v=tr[i], itt='auto', ott='auto')
            if trs[1]:
                mc.setKeyframe(f'{obj}.r{a}', t=frame, v=er[i], itt='auto', ott='auto')
            if trs[2]:
                mc.setKeyframe(f'{obj}.s{a}', t=frame, v=scl[i], itt='auto', ott='auto')
        if progress is not None:
            progress.setValue(int(frame) * 100 // count)
    mc.filterCurve(obj)
    return True


# Axis / matrix utilities

def hierarchical_sort(objlist: list = (), fromsel: bool = True) -> list:
    """
    Return objlist sorted in DAG (parent-before-child) order
    :param objlist:
    :param fromsel:
    :return: Sorted list
    """
    if fromsel:
        objlist = mc.ls(sl=True)

    if not objlist:
        return list(objlist)

    obj_set = set(objlist)
    rootlist = []
    for obj in obj_set:
        sl = om.MSelectionList()
        sl.add(obj)
        mfn = om.MFnDagNode(sl.getDagPath(0))
        rootlist.append(mfn.fullPathName().strip('|').split('|')[0])

    root = list(set(rootlist))[0]
    return [o for o in mc.ls(root, dag=True, tr=True) if o in obj_set]


def create_matrix(u: list | om.MVector, v: list | om.MVector, pnt: list | om.MPoint) -> om.MMatrix:
    """
    Build an orthonormal 4×4 matrix from two direction vectors and an origin
    :param u: Primary vector
    :param v: Secondary Vector
    :param pnt: Origin
    :return: 4x4 Matrix
    """
    u = om.MVector(u).normal()
    v = om.MVector(v)
    n = (u ^ v).normal()
    v = n ^ u
    matrix = list(u) + [0.0] + list(v) + [0.0] + list(n) + [0.0] + list(pnt)[:3] + [1.0]
    return om.MMatrix(matrix)


def reorder_matrix_rows(matrix: list | om.MMatrix, order: list = (0, 1, 2, 3)) -> om.MMatrix:
    """
    Permute the rows of a 4×4 matrix to remap axes
    :param matrix:
    :param order:
    """
    rows = [list(matrix)[i * 4: i * 4 + 4] for i in order]
    return om.MMatrix([v for row in rows for v in row])


def axis_to_vector(axis: str | None, point: bool = False) -> om.MVector | om.MPoint:
    """
    Convert an axis name ('-y') to om.MVector or om.MPoint
    :param axis: Signed axis such as '-y' or None for a null vector
    :param point: Return MPoint if True
    :return: MVector or MPoint
    """
    v = [0.0, 0.0, 0.0]
    if axis:
        idx = 'xyz'.index(axis.lstrip('-'))
        v[idx] = -1.0 if '-' in axis else 1.0
    return om.MPoint(v) if point else om.MVector(v)


def get_primary_axis(obj: str, typ: str = 'transform', tol: float = 0.001) -> str | None:
    """
    Guess the primary (bone) axis of obj from the average local position of
    its immediate children

    :param obj:
    :param typ:
    :param tol: tolerance

    :return: None if there are no children or the result is ambiguous
    """
    children = mc.listRelatives(obj, c=True, pa=True, typ=typ)
    if not children:
        return None

    v = om.MVector()
    for c in children:
        v += om.MVector(mc.getAttr(c + '.t')[0])
    v /= len(children)

    if v.length() < tol:
        return None

    comps = list(v)
    a = comps.index(max(comps))
    b = comps.index(min(comps))
    idx = b if abs(comps[b]) > abs(comps[a]) else a
    return ('-' if comps[idx] < 0 else '') + 'xyz'[idx]


def secondary_axis(axis: str) -> str:
    """
    Return the next axis in the cyclic order (xyzx...)
    The sign of axis is preserved
    :param axis:
    """
    next_axis = {'x': 'y', 'y': 'z', 'z': 'x'}[axis.lstrip('-')]
    return ('-' if '-' in axis else '') + next_axis


def get_axes_order(pa: str, sa: str) -> str:
    """
    Build a three-character axis-order string (for example 'xyz')
    from primary and secondary axes, filling in the third automatically
    :param pa: Primary axis
    :param sa: Secondary axis
    """
    axes = (pa + sa).replace('-', '')
    third = ''.join(a for a in 'xyz' if a not in axes)
    return axes + third


def clamp(a: float = 0.0, b: float = 1.0, x: float = -1) -> float:
    """
    Clamp x between a and b
    :param a: min value
    :param b: max value
    :param x: value to clamp
    :return: clamped value
    """
    return min(max(x, a), b)


def get_fps() -> float:
    """
    Return the scene frame rate as a float
    """
    fps_table = {
        'game': 15, 'film': 24, '23.976fps': 23.976,
        'pal': 25, 'ntsc': 30, 'show': 48, 'palf': 50, 'ntscf': 60,
    }
    return fps_table[mc.currentUnit(q=True, t=True)]


def scl_mat(mat: om.MMatrix, scl: float = 1.0) -> om.MMatrix:
    """
    Apply scaling factor on a matrix translation
    :param mat:
    :param scl:
    :return:
    """
    tm = om.MTransformationMatrix(om.MMatrix(mat))
    return tm.setTranslation(tm.translation(om.MSpace.kWorld) * scl, om.MSpace.kWorld).asMatrix()


# Utility functions

def shorten(name: str) -> str:
    return name.split('|')[-1]
