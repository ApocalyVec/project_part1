import math
import queue
from os import system


def inference(var, value, csp):
    """
    inference using ac_3, it is very similar to ac_3 except inference only checks the assigned value. Inference is a
    special case of ac_3
    :param Variable var:
    :param String value:
    :param runtimecsp csp:
    :return: Boolean; False if a var's domain results in empty
    """
    arcs = queue.Queue()
    for c in csp.get_arcs(var):
        arcs.put(c)

    while not arcs.empty():
        arc = arcs.get()
        if inference_revise(value, arc[0], arc[1], csp):  # if revised
            if not arc[0].domain:
                return False
            for propagating_arc in csp.get_arcs(arc[0]):
                arcs.put(propagating_arc)

    return True


def get_affected_value_num(var, value, csp):
    """
    only considers neighbors, otherwise very similar to inference_revise
    pruned values
    :param var:
    :param value:
    :param csp:
    :return:
    """
    prune_count = 0
    connections = csp.get_connecting_vars(var)

    for c in connections:
        biconst = csp.get_biconst(c, var)
        if biconst is not None:
            prune = False
            i = csp.get_index_of_value(value)

            for j in range(csp.get_values_len()):
                if value in c.domain:
                    prune = prune or biconst[i, j]
            if not prune:
                prune_count = prune_count + 1

    return prune_count

    # prune_list = []
    # var_prune_value = {}
    # arcs = queue.Queue()
    #
    # for c in csp.get_arcs(var):
    #     arcs.put(c)
    #
    # while not arcs.empty():
    #     arc = arcs.get()
    #     pruning_value = inference_prune_list(value, arc[0], arc[1], var_prune_value, csp)
    #     if pruning_value is not None:  # if revised
    #         prune_list.append(pruning_value)
    #         if not arc[0].domain:
    #             return len(prune_list)  # TODO this value should not be considered
    #         for propagating_arc in csp.get_arcs(arc[0]):
    #             arcs.put(propagating_arc)
    #
    # return len(prune_list)

#
# def inference_prune_list(value, x, y, var_prune_value, csp):
#     """
#     return the list of value that needs to be pruned from x's domain given that the value assigned to x is @param value
#     :param value:
#     :param x:
#     :param y:
#     :param csp:
#
#     :usage: this function is called by revise which is called by ac_3
#     """
#     pruning_value = None
#     biconst = csp.get_biconst(x, y)
#
#     # check the unary constraint first,
#     # The binary constraint covers the unary constraint
#     uex = csp.get_uex(x)
#     uin = csp.get_uin(x)
#
#     # now check the binary constraints
#     if biconst is not None:
#         prune = False
#         i = csp.get_index_of_value(value)
#
#         for j in range(csp.get_values_len()):
#             if x in var_prune_value.keys():
#                 if csp.get_value_by_index(j) in y.domain and csp.get_value_by_index(j) not in var_prune_value[
#                     x]:  # if the value is still in y's domain
#                     prune = prune or biconst[i, j]
#             else:
#                 if csp.get_value_by_index(j) in y.domain:  # if the value is still in y's domain
#                     prune = prune or biconst[i, j]
    #
    #     if not prune:
    #         pruning_value = value
    # if x in var_prune_value.keys():
    #     if pruning_value not in var_prune_value[x]:
    #         var_prune_value[x].append(pruning_value)
    # else:
    #     var_prune_value[x] = [pruning_value]
    #
    # return pruning_value


def inference_revise(value, x, y, csp):
    """
    return boolean
    :param value:
    :param x:
    :param y:
    :param csp:

    :usage: this function is called by revise which is called by ac_3
    """
    pruning_value = []
    biconst = csp.get_biconst(x, y)

    # check the unary constraint first,
    # The binary constraint covers the unary constraint
    uex = csp.get_uex(x)
    uin = csp.get_uin(x)

    if uex:
        if value in csp.get_uex(x):
            pruning_value.append(value)
    if uin:
        if value not in csp.get_uin(x):
            pruning_value.append(value)

    # now check the binary constraints
    if biconst is not None:
        prune = False
        i = csp.get_index_of_value(value)

        for j in range(csp.get_values_len()):
            if csp.get_value_by_index(j) in y.domain:  # if the value is still in y's domain
                prune = prune or biconst[i, j]

        if not prune:
            pruning_value.append(value)
    # TODO prune_value needs not to be a list
    for pv in pruning_value:
        x.prune_value(pv)

    return not not pruning_value


# TODO arcs should not have duplicate arcs
def ac_3(csp):
    """
    apply Arc Consistency to the given list of variables
    :param runtimecsp csp: constraint object against which to check arc consistency
    :return None, it modifies the domain of the given variable to be arc consistent
    """
    arcs = queue.Queue()

    # put arcs in the queue
    for a in csp.get_all_arcs():
        arcs.put(a)

    while not arcs.empty():
        arc = arcs.get()
        if revise(arc[0], arc[1], csp):  # revising the domain of arc[0]
            if not arc[0].domain:
                return False
            for propagating_arc in csp.get_arcs(arc[0]):
                arcs.put(propagating_arc)

    return True


# def revise(x, y, csp):
#     """
#         revise the domain of x, NOTE that it only checks the unary constraint for variables that are connected with arcs
#         :param x Variable
#         :param y Variable
#         :return bool true iff we revised the domain of x
#     """
#     pruning_value = []
#     biconst = csp.get_biconst(x, y)
#
#     for value in x.domain:
#
#         # check the unary constraint first,
#         # The binary constraint covers the unary constraint
#         uex = csp.get_uex(x)
#         uin = csp.get_uin(x)
#
#         if uex:
#             if value in csp.get_uex(x):
#                 pruning_value.append(value)
#         if uin:
#             if value not in csp.get_uin(x):
#                 pruning_value.append(value)
#
#         # now check the binary constraints
#         if biconst is not None:
#             prune = False
#             i = csp.get_index_of_value(value)
#
#             for j in range(csp.get_values_len()):
#                 if csp.get_value_by_index(j) in y.domain:  # if the value is still in y's domain
#                     prune = prune or biconst[i, j]
#
#             if not prune:
#                 pruning_value.append(value)
#
#     for pv in pruning_value:
#         x.prune_value(pv)
#
#     return not not pruning_value  # return true if revised

def revise(x, y, csp):
    """
        revise the domain of x, NOTE that it only checks the unary constraint for variables that are connected with arcs
        :param x Variable
        :param y Variable
        :return bool true iff we revised the domain of x
    """
    rtn = False
    for value in x.domain:
        revised = inference_revise(value, x, y, csp)
        rtn = rtn or revised

    return not not rtn  # return true if revised


def backtrack(assignment, csp):
    """
    NOTE that the Constraint object keeps all the variables. Thus it also keeps all the assignment to variables
    :param assignment:
    :param csp:
    :return:
    """
    if is_assignment_complete(assignment): return assignment
    var = select_unassigned_var(assignment, csp)
    for value in ordered_domain(var, csp):
        if check_value_consistency(var, value, assignment, csp):
            assignment[var] = value

            if not check_deadline(assignment, csp):
                assignment[var] = None
                return None

            if inference(var, value, csp):  # if inference left any variable's domain to be empty
                result = backtrack(assignment, csp)  # recursion call
                if result is not None:
                    return result

            assignment[var] = None  # remove this assignment

    return None


def ordered_domain(var, csp):
    """
    order the domain of a variable by the rule of least constraining value
    :param var:
    :param assignment:
    :param csp:
    :return:
    """
    for value in csp.get_values():
        print("Num: " + str(get_affected_value_num(var, value, csp)))
    #TODO have runtimecsp encapsulate this
    var.domain.sort(key=lambda x: get_affected_value_num(var, x, csp), reverse=True)
    return var.domain


def naive_select_unassigned_var(assignment, csp):
    '''
    naive select_unassigned_var
    :param Constraint csp
    '''
    for var in csp.get_all_variables():
        if assignment[var] is None:
            return var


def select_unassigned_var(assignment, csp):
    '''
    clever select_unassigned_var
    implementing minimum remaining-values (MRV) / most constrained variable / fail-first
    :param csp Constraint
    :param assignment Dictionary
    '''
    # make a list to order all the variables
    var_list = []
    min_domain_len = math.inf
    for var in csp.get_all_variables():
        if assignment[var] is None:
            var_list.append(var)
            if len(var.domain) < min_domain_len:  # update the min domain length
                min_domain_len = len(var.domain)

    min_var_list = []  # the list that keeps the most constrained variables
    for var in var_list:
        if len(var.domain) == min_domain_len:
            min_var_list.append(var)

    if len(min_var_list) == 1:  # just return the variable if there's one most constrained variable
        return min_var_list[0]
    elif len(min_var_list) > 1:  # break tie using Degree Heuristic
        min_var_list.sort(key=lambda x: (len(csp.get_connecting_vars(x))), reverse=True)
        return min_var_list[0]
    else:
        print("Solver: select_unassigned_var: bad var list")
        system.exit()


def is_assignment_complete(assignment):
    rtn = True
    for key, value in assignment.items():
        if value is None:
            rtn = rtn and False
        else:
            rtn = rtn and True
    return rtn


def initialize_assignment(assignment, csp):
    for var in csp.get_all_variables():
        assignment[var] = None


def check_value_consistency(var, value, assignment, csp):
    uex = csp.get_uex(var)
    uin = csp.get_uin(var)

    if uex:  # if the uex exists for this variable
        if value in uex:
            return False
    if uin:  # if the uex exists for this variable
        if value not in uin:
            return False

    connecting_var = csp.get_connecting_vars(var)

    # TODO the following part checks the binary constraints,
    # TODO it is very similar to what happended in revise function use in ac3
    rtn = True  # only using in this part
    if connecting_var is not None:  # if the variable has connections
        i = csp.get_index_of_value(value)  # get the index of the value being checked

        for c in connecting_var:
            const_matrix = csp.get_biconst(var, c)  # note that by doing this, var is the y axis, c is the x axis

            if assignment[c] is not None:
                rtn = const_matrix[i, csp.get_index_of_value(assignment[c])]
            else:
                for j in range(csp.get_values_len()):
                    if csp.get_value_by_index(j) in c.domain:
                        rtn = rtn or const_matrix[i, j]

    # The following are domain-specific code for the task-processor problem
    # process_time = 0
    # for v in csp.get_all_variables():
    #     if assignment[v] is not None:
    #         if assignment[v] == value:
    #             process_time = process_time + v.tag
    # if process_time + var.tag >

    return rtn

def check_deadline(assignment, csp):
    if not csp.is_deadline_met(assignment):
        return False
    else:
        return True