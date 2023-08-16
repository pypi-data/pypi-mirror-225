############################################################################
# Created by :  Okhtay alizadeh arasi
# LinkedIn URL: linkedin.com/in/oktai-alizade-94aa5538
# Mobile - whatsapp: +989144011724
# Telegram channel: https://t.me/OKprograms
# Instagram: opensees_apps
############################################################################

import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import os

def __find_nodes(ops, xlim=[], ylim=[], zlim=[]):

    if len(xlim) not in [0, 2]:
        print('xlim must be an empty list(default) or a list with two float number. default will be used ')
        xlim = []

    if len(zlim) not in [0, 2]:
        print('zlim must be an empty list(default) or a list with two float number. default will be used ')
        zlim = []

    if len(ylim) not in [0, 2]:
        print('ylim must be an empty list(default) or a list with two float number. default will be used ')
        ylim = []

    nodeTags = []
    for nod in ops.getNodeTags():
        xyz = ops.nodeCoord(nod)
        if len(xyz) == 2:
            xyz.append(0.0)

        add_node = True
        if len(xlim) != 0:
            for xx in [xyz[0]]:
                if xx < xlim[0] or xx > xlim[1]:
                    add_node = False
        if len(ylim) != 0:
            for yy in [xyz[1]]:
                if yy < ylim[0] or yy > ylim[1]:
                    add_node = False
        if len(zlim) != 0:
            for zz in [xyz[2]]:
                if zz < zlim[0] or zz > zlim[1]:
                    add_node = False

        if add_node != False:
            nodeTags.append(nod)

    if len(nodeTags) == 0:
            return False
    else:
        return nodeTags


def __find_elements(ops, xlim=[], ylim=[], zlim=[]):
    if len(xlim) not in [0, 2]:
        print('xlim must be an empty list(default) or a list with two float number. default will be used ')
        xlim = []

    if len(zlim) not in [0, 2]:
        print('zlim must be an empty list(default) or a list with two float number. default will be used ')
        zlim = []

    if len(ylim) not in [0, 2]:
        print('ylim must be an empty list(default) or a list with two float number. default will be used ')
        ylim = []

    eleTags = []
    for ele in ops.getEleTags():
        elenodes = ops.eleNodes(ele)
        XX = []
        YY = []
        ZZ = []
        for nod in elenodes:
            xyz = ops.nodeCoord(nod)
            XX.append(xyz[0])
            YY.append(xyz[1])
            if len(xyz) == 2:
                ZZ.append(0.0)
            else:
                ZZ.append(xyz[2])

        add_ele = True
        if len(xlim) != 0:
            for xx in [XX]:
                if xx < xlim[0] or xx > xlim[1]:
                    add_ele = False
        if len(ylim) != 0:
            for yy in [YY]:
                if yy < ylim[0] or yy > ylim[1]:
                    add_ele = False
        if len(zlim) != 0:
            for zz in [ZZ]:
                if zz < zlim[0] or zz > zlim[1]:
                    add_ele = False

        if add_ele != False:
            eleTags.append(ele)

    if len(eleTags) == 0:
        return False
    else:
        return eleTags


def damping(ops, xDamp, T1=0, T2=0, factor_betaK=0.0, factor_betaKinit=0.0, factor_betaKcomm=1.0,
            xlim=[], ylim=[], zlim=[], solver='-genBandArpack'):
    """
    A function for applying damping to the structure. Program calculates mass and stiffness coefficients(alphaM and betaK)
    based on first and second periods. Rayleigh damping parameters are assigned to the nodes and elements in the region
    defined by xlim, ylim and zlim.

    ops: openseespy object. Alias for this package shouldbe ops(import openseespy.opensees as ops).
    xDamp: Damping ratio
    T1: Period at first mode (Optional, default value is 0. If T1 = 0 and T2 = 0, program will perform eigen analysis to
        find T1 and T2).
    T2: Period at second mode (Optional, default value is 0. If T1 = 0 and T2 = 0, program will perform eigen analysis to
        find T1 and T2).
    factor_betaK: Factor applied to elements current stiffness matrix = factor_betaK * betaK(Optional, default value is 0.0)
    factor_betaKinit: Factor applied to elements initial stiffness matrix = factor_betaKinit * betaK(Optional, default value is 0.0)
    factor_betaKcomm: Factor applied to elements committed stiffness matrix = factor_betaKcomm * betaK(Optional, default value is 1.0)
    xlim: An empty list or a list contains xmin and xmax of the region.(Optional, default value is an empty list)
    ylim: An empty list or a list contains ymin and ymax of the region.(Optional, default value is an empty list)
    zlim: An empty list or a list contains zmin and zmax of the region.(Optional, default value is an empty list)
    solver: String detailing type of solver: '-genBandArpack', '-fullGenLapack', (Optional, default value is '-genBandArpack')

    return: alphaM, betaK, lambda, omega, Tn
    """

    if T1 == 0 or T2 == 0:
        lambdaN, omega, Tn = eigen(ops, 2, solver=solver)
        omegaI, omegaJ = omega
    else:
        omegaI, omegaJ = (2 * np.pi) / T1, (2 * np.pi) / T2
        lambdaN = [omegaI ** 2, omegaJ ** 2]
        Tn = [T1, T2]
        omega = [omegaI, omegaJ]

    alphaM = xDamp * (2 * omegaI * omegaJ) / (omegaI + omegaJ)
    betaSt = 2 * (xDamp / (omegaI + omegaJ))

    if len(xlim) == 0 and len(ylim) == 0 and len(zlim) == 0:
        ops.rayleigh(alphaM, factor_betaK * betaSt, factor_betaKinit * betaSt, factor_betaKcomm * betaSt)
    else:
        dnodes = __find_nodes(ops, xlim, ylim, zlim)
        if dnodes is False:
            return

        delements = __find_elements(ops, xlim, ylim, zlim)
        if delements is False:
            return

        ops.region(1, '-ele', *delements, '-rayleigh', 0.0, factor_betaK * betaSt,
                   factor_betaKinit * betaSt, factor_betaKcomm * betaSt)
        ops.region(2, '-node', *dnodes, '-rayleigh', alphaM, 0.0, 0.0, 0.0)

    return alphaM, betaSt, lambdaN, omega, Tn


def eigen(ops, num_Modes, solver='-genBandArpack'):
    """
    Function to perform eigen analysis.

    ops: openseespy object. Alias for this package shouldbe ops(import openseespy.opensees as ops).
    num_Modes: Number of eigenvalues required.
    solver: String detailing type of solver: '-genBandArpack', '-fullGenLapack', (Optional, default value is '-genBandArpack')
    return: lambda, omega, Tn
    """
    print('######################')
    print('### Eigen Analysis ###')
    print('######################')

    start_time = datetime.now().replace(microsecond=0)
    print('Start Time: {}'.format(start_time))

    lambdaN = ops.eigen(solver, num_Modes)
    omega = []
    Tn = []
    for i in range(num_Modes):
        lambdaI = lambdaN[i]
        omega.append(pow(lambdaI, 0.5))
        tt = (2 * np.pi) / pow(lambdaI, 0.5)
        Tn.append(tt)
        print('T' + str(i+1) + ' = ' + str(round(tt, 3)) + '     f' + str(i+1) + ' = ' + str(round(1 / tt, 3)))

    end_time = datetime.now().replace(microsecond=0)
    print('End Time: {}'.format(end_time))
    print('Duration: {}'.format(end_time - start_time))

    return lambdaN, omega, Tn


def plot_protocol(ax, filename_protocol, Dy):
    """
    Function to plot loading protocol used in pushover cyclic analysis.

    ax: The axes on which the protocol is drawn.
    filename_protocol: A two-column data file including steps and displacements.
    Dy: Yield displacement.
    """
    step = []
    disp = []
    with open(filename_protocol) as f:
        lines = f.readlines()
    for line in lines:
        line2 = line.split()

        step.append(float(line2[0]))
        disp.append(float(line2[1]))

    f.close()

    target = [x * Dy for x in disp]

    ax.plot(step, target)
    ax.set_xlabel('step')
    ax.set_ylabel('D')
    ax.grid('on')


def plot_record(ax, filename_record, factor=1, xtitle='time(s)', ytitle='acceleration(g)', title=''):
    time = []
    acceleration = []
    with open(filename_record) as f:
        lines = f.readlines()
    for line in lines:
        line2 = line.split()

        time.append(float(line2[0]))
        acceleration.append(float(line2[1]) * factor)

    f.close()

    ax.plot(time, acceleration, linewidth=0.5)
    ax.set_xlabel(xtitle)
    ax.set_ylabel(ytitle)
    ax.set_title(title)
    ax.grid('on')

def analyze_static(ops, analysis_option, num_steps=10, loadConst='yes', time=0.0):
    """
    Function to perform static analysis.

    ops: openseespy object. Alias for this package shouldbe ops(import openseespy.opensees as ops).
    analysis_option: A python dictionary contains analysis options.
         Example:
         analysis_option = {'constraints': ['Plain'],
                            'numberer': ['Plain'],
                            'system': ['BandGeneral'],
                            'test': ['NormUnbalance', 1.0e-5, 1000],
                            'algorithm': ['NewtonLineSearch']}
    num_steps: Number of analysis steps to perform(Optional, default value is 10).
    loadConst: Is used to set the loads constant in the domain. Valid values are 'yes', 'y', 'no' or 'n'.
        (Optional, default value is 'yes').
    time: Time domain is to be set to(Optional, default value is 0.0).
    """
    print('##########################')
    print('### Static Analysis')
    print('##########################')

    logfilename = 'opslogfile.txt'
    ops.logFile(logfilename, '-noEcho')

    start_time = datetime.now().replace(microsecond=0)
    print('Start Time: {}'.format(start_time))

    ops.record()

    print('# Analysis Option:')
    ops.wipeAnalysis()
    print('ops.wipeAnalysis()')
    for key, vals in analysis_option.items():
        str_opt = 'ops.' + key + '('
        for i in range(len(vals) - 1):
            val = vals[i]
            if isinstance(val, str):
                str_opt = str_opt + "\'" + val + "\'" + ', '
            else:
                str_opt = str_opt + str(val) + ', '
        val = vals[-1]
        if isinstance(val, str):
            str_opt = str_opt + "\'" + val + "\'" + ')'
        else:
            str_opt = str_opt + str(val) + ')'

        print(str_opt)
        eval(str_opt)
    print("ops.integrator(\'LoadControl\', " + str(1 / num_steps) + ")")
    print("ops.analysis(\'Static\')")

    ops.integrator('LoadControl', 1 / num_steps)
    ops.analysis('Static')

    print('# Start Analysis: ')
    num_steps = int(num_steps)
    for step in range(num_steps):
        ok = ops.analyze(1)
        if ok != 0:
            print('    Analysis failed at step ' + str(step + 1) + '/' + str(num_steps))
            end_time = datetime.now().replace(microsecond=0)
            print('End Time: {}'.format(end_time))
            print('Duration: {}'.format(end_time - start_time))
            exit()

        print('    Analysis successful at step ' + str(step + 1) + '/' + str(num_steps))

    if loadConst.lower() in ['y', 'yes']:
         ops.loadConst('-time', time)

    ops.remove('recorders')

    print('Analysis successful')

    end_time = datetime.now().replace(microsecond=0)
    print('End Time: {}'.format(end_time))
    print('Duration: {}'.format(end_time - start_time))

def analyze_push_mono(ops, analysis_option, TargetDisp, cnodeTag, cdof, du_min, du_max, du_Div=2, numIter=10):
    """
    Function to perform pushover monotonic analysis.

    ops: openseespy object. Alias for this package shouldbe ops(import openseespy.opensees as ops).
    analysis_option: A python dictionary contains analysis options.
        Example:
        analysis_option = {'constraints': ['Plain'],
                           'numberer': ['Plain'],
                           'system': ['BandGeneral'],
                           'test': ['NormUnbalance', 1.0e-5, 1000],
                           'algorithm': ['NewtonLineSearch']}
    TargetDisp: pushover analysis is carried out on the structure until the displacement of the cnode equals to
        the TargetDisp(target displacement).
    cnodeTag: node whose response controls solution.
    cdof: degree of freedom at the node.
    du_min: the min stepsize the user will allow.
    du_max: the max stepsize the user will allow.
    du_Div:
    numIter: the number of iterations the user would like to occur in the solution algorithm(Optional, default value is 10).

    How it works?
    - Analysis is started with du = du_max.
    - If the analysis does not converge at a certain step, du is reduced by du_Div times(du = du / du_Div).
         This continues until the analysis converges at that step or du becomes smaller than du_min in which case the
         analysis is terminated.
    - After 10 successful steps du is increased by du_Div times(du = du * du_Div).
      This continues until du becomes greater that du_max in which case du will be set to du_max.
    - At the end, program adjusts du so that the location corresponds to the target displacement.

    """
    print('##########################')
    print('### Push Over Analysis ###')
    print('##########################')

    start_time = datetime.now().replace(microsecond=0)
    print('Start Time: {}'.format(start_time))

    logfilename = 'opslogfile.txt'
    ops.logFile(logfilename, '-noEcho')

    print('# Analysis Option:')
    ops.wipeAnalysis()
    print('ops.wipeAnalysis()')
    for key, vals in analysis_option.items():
        str_opt = 'ops.' + key + '('
        for i in range(len(vals) - 1):
            val = vals[i]
            if isinstance(val, str):
                str_opt = str_opt + "\'" + val + "\'" + ', '
            else:
                str_opt = str_opt + str(val) + ', '
        val = vals[-1]
        if isinstance(val, str):
            str_opt = str_opt + "\'" + val + "\'" + ')'
        else:
            str_opt = str_opt + str(val) + ')'
        print(str_opt)
        eval(str_opt)
    print('# Start Analysis: ')

    Nstep = 1
    node_location = 0

    if TargetDisp > node_location:
        du = du_max
    else:
        du = du_max * -1
    print('    du = ', str(du))

    ops.integrator('DisplacementControl', cnodeTag, cdof, du, numIter)
    ops.analysis('Static')

    num_suc = 0
    while round(abs(node_location - TargetDisp), 7) > 0:
        if abs(TargetDisp - node_location) < abs(du):
            du = TargetDisp - node_location
            print('    Try du = ', str(du))
            ops.integrator('DisplacementControl', cnodeTag, cdof, du, numIter)
            num_suc = 0

        if num_suc == 10:
            if abs(du * du_Div) <= du_max:
                du = du * du_Div
                ops.integrator('DisplacementControl', cnodeTag, cdof, du, numIter)
                print('    Try du = ', str(du))
                num_suc = 0

        ok = ops.analyze(1)
        if ok != 0:
            num_suc = 0
            print('    Analysis failed at step ', str(Nstep))
            du = du / du_Div
            if abs(du) < du_min:
                print('  Analysis failed: du < dumin ', '     Location = ', str(round(node_location, 7)),
                      '    Target = ', str(TargetDisp))

                end_time = datetime.now().replace(microsecond=0)
                print('End Time: {}'.format(end_time))
                print('Duration: {}'.format(end_time - start_time))

                exit()

            print('    Try du = ', str(du))
            ops.integrator('DisplacementControl', cnodeTag, cdof, du, numIter)
        else:
            node_location += du
            print('    Analysis successful at step ', str(Nstep), '     Location = ',
                  str(round(node_location, 7)), '    Target = ', str(TargetDisp))
            Nstep += 1
            num_suc += 1

    print('Analysis successful')

    end_time = datetime.now().replace(microsecond=0)
    print('End Time: {}'.format(end_time))
    print('Duration: {}'.format(end_time - start_time))

def analyze_push_cyclic(ops, analysis_option, filename_protocol, cnodeTag, cdof, Dy, du_min, du_max, du_Div=2,
                        numIter=10):
    """
    Function to perform pushover cyclic analysis.

    ops: openseespy object. Alias for this package shouldbe ops(import openseespy.opensees as ops).
    analysis_option: A python dictionary contains analysis options.
        Example:
        analysis_option = {'constraints': ['Plain'],
                           'numberer': ['Plain'],
                           'system': ['BandGeneral'],
                           'test': ['NormUnbalance', 1.0e-5, 1000],
                           'algorithm': ['NewtonLineSearch']}
    filename_protocol: A two-column data file including steps and displacements.
    cnodeTag: node whose response controls solution.
    cdof: degree of freedom at the node.
    Dy: Yield displacement
    du_min: the min stepsize the user will allow.
    du_max: the max stepsize the user will allow.
    du_Div:
    numIter: the number of iterations the user would like to occur in the solution algorithm(Optional, default value is 10).

    How it works?
    - Analysis is started with du = du_max.
    - If the analysis does not converge at a certain step, du is reduced by du_Div times(du = du / du_Div).
         This continues until the analysis converges at that step or du becomes smaller than du_min in which case the
         analysis is terminated.
    - After 10 successful steps du is increased by du_Div times(du = du * du_Div).
      This continues until du becomes greater that du_max in which case du will be set to du_max.
    - At the end of each cycle program adjusts du so that the location corresponds to the peak displacement in that cycle.

    """

    print('##########################')
    print('### Cyclic Analysis ###')
    print('##########################')

    start_time = datetime.now().replace(microsecond=0)
    print('Start Time: {}'.format(start_time))

    logfilename = 'opslogfile.txt'
    ops.logFile(logfilename, '-noEcho')

    step = []
    disp = []
    step_count = 1
    with open(filename_protocol) as f:
        lines = f.readlines()
    for line in lines:
        line2 = line.split()

        step.append(step_count)
        disp.append(float(line2[1]))
        step_count += 1

    f.close()

    if disp[0] == 0.0 and step[0] == 0:
        disp.pop(0)

    TargetDisp = [x * Dy for x in disp]

    print('# Analysis Option:')
    ops.wipeAnalysis()
    print('ops.wipeAnalysis()')
    for key, vals in analysis_option.items():
        str_opt = 'ops.' + key + '('
        for i in range(len(vals)-1):
            val = vals[i]
            if isinstance(val, str):
                str_opt = str_opt + "\'" + val + "\'" + ', '
            else:
                str_opt = str_opt + str(val) + ', '
        val = vals[-1]
        if isinstance(val, str):
            str_opt = str_opt + "\'" + val + "\'" + ')'
        else:
            str_opt = str_opt + str(val) + ')'

        print(str_opt)
        eval(str_opt)

    print('# Start Analysis: ')
    node_location = 0
    Nstep = 1
    for i in range(len(TargetDisp)):
        print('Step ' + str(i + 1) + '/' + str(len(TargetDisp)) + ':')
        if TargetDisp[i] > node_location:
            du = du_max
        else:
            du = du_max * -1

        if abs(TargetDisp[i] - node_location) < abs(du):
            du = TargetDisp[i] - node_location

        print('    Try du = ', str(du))
        ops.integrator('DisplacementControl', cnodeTag, cdof, du, numIter)
        ops.analysis('Static')

        num_suc = 0
        while round(abs(node_location - TargetDisp[i]), 7) > 0:
            du_end = TargetDisp[i] - node_location
            if abs(du_end) < abs(du):
                du = du_end
                print('    Try du = ', str(du))
                ops.integrator('DisplacementControl', cnodeTag, cdof, du, numIter)
                num_suc = 0

            if num_suc == 10:
                if abs(du * du_Div) <= du_max:
                    du = du * du_Div
                    if abs(du_end) < abs(du):
                        du = du_end

                    ops.integrator('DisplacementControl', cnodeTag, cdof, du, numIter)
                    print('    Try du = ', str(du))
                    num_suc = 0

            ok = ops.analyze(1)
            if ok != 0:
                num_suc = 0
                print('    Analysis failed at step ', str(Nstep))
                du = du / du_Div
                if abs(du) < du_min:
                    print('  Analysis failed: du < dumin =  ', str(du_min), '     Location = ', str(round(node_location, 6))
                          , '    Target = ', str(TargetDisp[i]*1000))

                    end_time = datetime.now().replace(microsecond=0)
                    print('End Time: {}'.format(end_time))
                    print('Duration: {}'.format(end_time - start_time))
                    exit()

                print('    Try du = ', str(du))
                ops.integrator('DisplacementControl', cnodeTag, cdof, du, numIter)
            else:
                node_location += du
                print('    Analysis successful at step ', str(Nstep), '     Location = ', str(round(node_location, 2)),
                          '    Target = ', str(TargetDisp[i]*1000))

                Nstep += 1
                num_suc += 1

    print('Analysis successful')

    end_time = datetime.now().replace(microsecond=0)
    print('End Time: {}'.format(end_time))
    print('Duration: {}'.format(end_time - start_time))

def analyze_transient(ops, analysis_option, filename_record, tag_timeseries, tag_pattern, factor=1.0, direction=1,
                      dt_min=0, dt_max=0, dt_Div=2, type='-accel'):
    """
    Function to perform transient analysis.

    ops: openseespy object. Alias for this package shouldbe ops(import openseespy.opensees as ops).
    analysis_option: A python dictionary contains analysis options.
        Example:
        analysis_option = {'constraints': ['Plain'],
                           'numberer': ['Plain'],
                           'system': ['BandGeneral'],
                           'test': ['NormUnbalance', 1.0e-5, 1000],
                           'algorithm': ['NewtonLineSearch']}
    filename_record: A two-column data file including times and values.
    tag_timeseries: Program creates a TimeSeries object of type path with tag_timeseries as its unique tag.
    tag_pattern: Program creates a pattern object of type UniformExcitation with tag_pattern as its unique tag.
    factor: A factor to multiply load factors by(Optional, default value is 1.0).
    direction: 	direction in which ground motion acts(Optional, default value is 1).
        1 - corresponds to translation along the global X axis
        2 - corresponds to translation along the global Y axis
        3 - corresponds to translation along the global Z axis
        4 - corresponds to rotation about the global X axis
        5 - corresponds to rotation about the global Y axis
        6 - corresponds to rotation about the global Z axis
    dt_min: minimum time steps (Optional, default value is 0.0).
    dt_max: maximum time steps(Optional, default value is 0.0).
    dt_Div:
    type: Type of the history. Valid values are '-disp', '-vel' or '-accel' (Optional, default value is '-accel').

    How it works?
    - Program calculates dt using data provided by user.
    - If dt_max=0 or dt_max > dt, program will set dt_max to dt.
    - If dt_min=0 or dt_min > dt  program will set dt_min to dt_max / 5.

    - Analysis is started with dt = dt_max.
    - If the analysis does not converge at a certain step, dt is reduced by dt_Div times(dt = dt / dt_Div).
         This continues until the analysis converges at that step or dt becomes smaller than dt_min in which case the
         analysis is terminated.
    - After 10 successful steps dt is increased by dt_Div times(dt = dt * du_Div).
      This continues until dt becomes greater that dt_max in which case dt will be set to dt_max.
    """

    print('##########################')
    print('### Transient Analysis ###')
    print('##########################')

    start_time = datetime.now().replace(microsecond=0)
    print('Start Time: {}'.format(start_time))

    logfilename = 'opslogfile.txt'
    ops.logFile(logfilename, '-noEcho')

    time = []
    acceleration = []
    with open(filename_record) as f:
        lines = f.readlines()
    for line in lines:
        line2 = line.split()
        time.append(float(line2[0]))
        acceleration.append(float(line2[1]))

    f.close()

    _dt = time[1] - time[0]

    filename_temp = '__temprecordfile.txt'
    if os.path.exists(filename_temp):
        os.remove(filename_temp)

    with open(filename_temp, 'w') as f:
        for acc in acceleration:
            f.write(f"{acc}\n")

    # Set time series to be passed to uniform excitation
    str_timeSeries = "ops.timeSeries(\'Path\'," + ' ' + str(tag_timeseries) + ", \'-filePath\' ,\'" + filename_temp + \
                     "', \'-dt\', " + str(_dt) + ", \'-factor\', " + str(factor) + ")"
    print(str_timeSeries)
    eval(str_timeSeries)
    # ops.timeSeries('Path', tag_timeseries, '-filePath', filename_temp, '-dt', _dt, '-factor', factor)

    # Create UniformExcitation load pattern
    #                         tag dir
    # ops.pattern('UniformExcitation',  tag_pattern,  direction,  type, tag_timeseries)
    str_pattern = "ops.pattern(\'UniformExcitation\', " + str(tag_pattern) + ', ' + str(direction) + ', \'' + type + \
                  '\', ' + str(tag_timeseries) + ')'
    print(str_pattern)
    eval(str_pattern)

    print('# Analysis Option:')
    ops.wipeAnalysis()
    print('ops.wipeAnalysis()')
    for key, vals in analysis_option.items():
        str_opt = 'ops.' + key + '('
        for i in range(len(vals)-1):
            val = vals[i]
            if isinstance(val, str):
                str_opt = str_opt + "\'" + val + "\'" + ', '
            else:
                str_opt = str_opt + str(val) + ', '
        val = vals[-1]
        if isinstance(val, str):
            str_opt = str_opt + "\'" + val + "\'" + ')'
        else:
            str_opt = str_opt + str(val) + ')'

        print(str_opt)
        eval(str_opt)

    print('# Start Analysis: ')

    if dt_max <= 0:
        print('### dt_max <= 0.0, dt_max was set to dt = ' + str(_dt))
        dt_max = _dt

    if dt_max > _dt:
        print("Warning: ")
        print('### dt_max = ' + str(dt_max) + '   dt = ' + str(_dt) + '  dt_max > dt')

    if dt_min <= 0:
        print('### dt_min <= 0.0, dt_min was set to dt_max / 10')
        dt_min = dt_max / 10

    if dt_min > _dt:
        print('### dt_min >  dt, dt_min was set to dt_max / 10')
        dt_min = dt_max / 10

    if dt_min > dt_max:
        print('### dt_min >  dt_max, dt_min was set to dt_max / 10')
        dt_min = dt_max / 10

    print('    dt = ', str(dt_max))

    dt = dt_max
    ops.analysis('Transient')

    Nstep = 1
    time_final = time[-1]
    time_cur = 0
    num_suc = 0

    while round(time_final - time_cur, 7) > 0:
        dt_end = time_final - time_cur
        if dt_end < dt:
            dt = dt_end
            print('    Try dt = ', str(dt))
            num_suc = 0

        if num_suc == 10:
            if dt * dt_Div <= dt_max:
                dt = dt * dt_Div
                if dt_end < dt:
                    dt = dt_end

                print('    Try dt = ', str(dt))
                num_suc = 0

        ok = ops.analyze(1, dt)
        if ok != 0:
            print('    Analysis failed at step ', str(Nstep), '   time = ', str(time_cur))
            dt = dt / dt_Div
            if abs(dt) < dt_min:
                print('  Analysis failed: dt < dtmin ', '   time = ', str(time_cur))
                end_time = datetime.now().replace(microsecond=0)
                print('End Time: {}'.format(end_time))
                print('Duration: {}'.format(end_time - start_time))

                exit()

            print('    Try dt = ', str(dt))
            num_suc = 0
        else:
            time_cur += dt
            print('    Analysis successful at step ', str(Nstep), '   time = ', str(time_cur))
            Nstep += 1
            num_suc += 1

    print('Analysis successful')
    end_time = datetime.now().replace(microsecond=0)
    print('End Time: {}'.format(end_time))
    print('Duration: {}'.format(end_time - start_time))