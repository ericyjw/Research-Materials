# format:
# index = store
# sub-array = estimated profit for store n for 0...m boxes
import copy
estimated_profit = [
    [0, 4, 6, 7, 7, 7, 7],
    [0, 2, 4, 6, 8, 9, 10],
    [0, 6, 8, 8, 8, 8, 8],
    [0, 2, 3, 4, 4, 4, 4],
]

# Problem:
# The owner of a chain of four grocery stores has purchases six crates of fresh berries
# The owner does not wish to split crates between stores, but is willing to make zero allocations.
# Find the allocation of the size crates so as to maximise the profits

# Math:
# m1, m2, m3, m4 are the num of crates allocated to store1, store2, store3 and store4 respectively
# f1(m1), f2(m2), f3(m3), f4(m4) are the respective profit from the stores

# Objective:
# Maximise Z = f1(m1) + f2(m2) + f3(m3) + f4(m4)

# Constraints:
# m1 + m2 + m3 + m4 <= 6
# m1, m2, m3, m4 >= 0
memo = {}


def initialise_memo(memo, curr):
    for resource in range(len(curr)):
        reward = curr[resource]
        if resource not in memo:
            memo[resource] = {'reward': reward, 'combi': [[resource]]}
        else:
            if reward > memo[resource]['reward']:
                memo[resource]['reward'] = reward
                memo[resource]['combi'] = [resource]
            elif reward == memo[resource]['reward']:
                memo[resource]['combi'].append([resource])

def update_tabulation(tabulation, memo, curr):
    for allocated_resource in memo:
        for extra_resource in range(len(curr)):
            reward = curr[extra_resource]
            total_reward = memo[allocated_resource]['reward'] + reward
            total_resource = allocated_resource + extra_resource

            if total_resource > 6:       # contraint: x1 + x2 + x3 + x4 <= 6
                break

            # There is no total_reward added to total_resource tabulation
            if total_resource not in tabulation:
                tabulation[total_resource] = {}
                prev_combi = memo[allocated_resource]['combi']

                for combi in prev_combi:
                    new_combi = copy.deepcopy(combi)
                    new_combi.append(extra_resource)
                    tabulation[total_resource]['reward'] = total_reward
                    tabulation[total_resource]['combi'] = [new_combi]

            # There is an existing total_reward added to total_resource tabulation
            # Update the existing total_reward & combination
            else:
                # Only update when the newly calculated total_reward > memo stored total_reward
                if total_reward > tabulation[total_resource]['reward']:
                    tabulation[total_resource]['reward'] = total_reward
                    # Replace existing combinations
                    tabulation[total_resource]['combi'].clear()
                    prev_combi = memo[allocated_resource]['combi']
                    for combi in prev_combi:
                        new_combi = copy.deepcopy(combi)
                        new_combi.append(extra_resource)
                        tabulation[total_resource]['combi'].append(new_combi)

                elif total_reward == tabulation[total_resource]['reward']:
                    tabulation[total_resource]['reward'] = total_reward
                    prev_combi = memo[allocated_resource]['combi']
                    for combi in prev_combi:
                        new_combi = copy.deepcopy(combi)
                        new_combi.append(extra_resource)
                        tabulation[total_resource]['combi'].append(new_combi)

def update_memo(tabulation, memo):
    for allocated_resource in tabulation:
        # First entry
        if allocated_resource not in memo:
            memo[allocated_resource] = {}
            memo[allocated_resource]['reward'] = tabulation[allocated_resource]['reward']
            memo[allocated_resource]['combi'] = tabulation[allocated_resource]['combi']
        # Update max total_profit & combination
        elif tabulation[allocated_resource]['reward'] >= memo[allocated_resource]['reward']:
            memo[allocated_resource]['reward'] = tabulation[allocated_resource]['reward']
            memo[allocated_resource]['combi'] = tabulation[allocated_resource]['combi']

def calculateOptimalSol(memo):
    for curr in estimated_profit:
        tabulation = {}

        if (not memo):
            initialise_memo(memo, curr)
            continue

        update_tabulation(tabulation, memo, curr)
        update_memo(tabulation, memo)
   
def printOptimalSol(memo):
    max = 0
    max_total = []
    optimal_combi = []
    for total_resource in memo:
        if memo[total_resource]['reward'] > max:
            max = memo[total_resource]['reward']
            max_total = [total_resource]
        elif memo[total_resource]['reward'] == max:
            max_total.append(total_resource)

    print('===== Optimal Solution =====')
    for mt in max_total:
        print('Total Resource: {}'.format(mt))
        print('Total Reward: {}'.format(max))
        print('Combinations:')
        for combi in memo[mt]['combi']:
            print(combi)

calculateOptimalSol(memo)
printOptimalSol(memo)
