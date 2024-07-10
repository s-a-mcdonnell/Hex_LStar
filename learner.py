from teacher import Teacher

import itertools as it
import matplotlib.pyplot as plt
import networkx as nx

##############################################################################################################

class Learner:

    ##########################################################################################################

    # Draws current m_hat
    def draw_graph(self):

        print("draw graph called.")

        # turn the m_hat array into the graph (add appropriate nodes and edges based on table)
        m_graph = nx.MultiDiGraph(directed = True)

        accepting = []

        for row in self.m_hat:
            # create node with label from the index, and add it to the list of accepted nodes if row[0] is 1

            access_string = next(key for key in self.access_string_reference.keys() if self.access_string_reference[key] == self.m_hat.index(row))
            print(access_string)

            m_graph.add_node(self.m_hat.index(row), data=access_string)
            if row[0] == 1:
                accepting.append(self.m_hat.index(row))

            # edge from node "row index" to node "row[i]" where it is labelled by the character in language[i]
            for i in range(1, len(row)):
                print(self.alphabet[i-1])
                m_graph.add_edge(self.m_hat.index(row), row[i], key = self.alphabet[i - 1], data = self.alphabet[i-1])

        # draw the graph

        colors_node = []
        for node in m_graph:
            if node in accepting:
                colors_node.append('green')
            else:
                colors_node.append('red')

        labels_node = {n : data["data"] for n, data in m_graph.nodes(data = True)}

        labels = {(u, v, key): data["data"] for u, v, key, data in m_graph.edges(keys = True, data = True)}

        pos = nx.shell_layout(m_graph)
        connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)]
        # ^^^ from this multigraph tutorial https://networkx.org/documentation/stable/auto_examples/drawing/plot_multigraphs.html
        
        nx.draw_networkx_nodes(m_graph, pos, node_color=colors_node)
        nx.draw_networkx_labels(m_graph, pos, labels_node, font_size=10)

        nx.draw_networkx_edges(m_graph, pos, edge_color="grey", connectionstyle=connectionstyle)
        nx.draw_networkx_edge_labels(m_graph, pos, labels, label_pos=0.25, font_size = 10, font_color="black", connectionstyle=connectionstyle, bbox={"alpha": 0})

        plt.show()
        print("plot printed.")
    
    ##########################################################################################################

    def __init__(self, alphabet = ['0','1'], num_states = -1, seed = -1, premade_dfa = None, display_graphs = False):

        self.solved = False
        # Intialize alphabet
        self.alphabet = alphabet

        # Whether or not to draw the graphs
        self.graphs = display_graphs

        # Note that the alphabet must contains characters (strings of length one), not longer strings or ints
        for character in alphabet:
            assert type(character) is str
            assert len(character) == 1
        

        # Initialize teacher

        # If a premade DFA was provided (for testing), use it
        if premade_dfa:
            assert len(premade_dfa[0]) == len(alphabet) + 1

            self.my_teacher = Teacher(self.alphabet, premade_dfa = premade_dfa)

        
        # Else the DFA to be learned will be constructed by the teacher
        else:
            self.my_teacher = Teacher(self.alphabet, num_states = num_states, seed = seed)

        # Initialize binary classifcation tree T and tentative hypothesis M_hat
        self.init_t_m_hat()

        # Confirm that all -1s with which M_hat was initialized have been overwritten
        for row in self.m_hat:
            for entry in row:
                assert entry >= 0
        
        # print("m_hat at end of initialization: " + str(self.m_hat))

        print("Learner initialization complete")

    ##########################################################################################################

    # Initialize T and M_hat
    # Helper method for contructor
    def init_t_m_hat(self):
        # initialize T with just the empty string (lambda)
        self.t = Tree(Node("", None, 0))

        # create M_hat with just one state in T
        # The DFA (M) is a matrix in which the rows are the nodes
        # The first entry in each row is a boolean in int form (0 or 1) indicating whether the node is an accept (1) or reject (0) state
        # The remaining entries in each row are the numbers of the nodes which the corresponding alphabet value at that index points to
        self.m_hat = []

        # dictionary for storing access strings as keys corresponding to their rows in the m_hat matrix
        # add to the dictionary when updating the tree, not when reconstructing m_hat, because we need dict to construct m_hat
        self.access_string_reference = {}
        self.update_dictionary("", 0)

        # Create the first state (with the empty access string)
        # check whether empty string is accepted or rejected
        to_append = []
        if self.my_teacher.member(""):
            # empty string accepted
            to_append.append(1)
        else:
            to_append.append(0)
        
        # This initial state points only to itself
        for i in range(len(self.alphabet)):
            to_append.append(0)

        # Append the first state to M_hat        
        self.m_hat.append(to_append)

        print("m hat table: " + str(self.m_hat))
        print("access dictionary: " + str(self.access_string_reference))

        # draw m_hat graph here, as m_hat is not updated in initialization past this point
        if self.graphs:
            self.draw_graph()
    
        # equivalence query on initial M_hat
        gamma = self.my_teacher.equivalent(self.m_hat)

        # If there is no counterexample, we have solved the DFA
        if not gamma:
            print("We are done. DFA is the trivial DFA.")
            self.solved = True
        
        # Else put counterexample gamma into our tree T
        else:

            assert type(gamma) is str

            assert(self.my_teacher.member(gamma) != self.my_teacher.member(gamma, self.m_hat, self.alphabet))


            # print("Counterexample found, adding to tree.")
            if self.my_teacher.member(gamma):
                self.t.root.right_child = Node(gamma, self.t.root, 1)
                self.t.root.left_child = Node("", self.t.root, 1)
            else:
                # counterexample is rejected
                self.t.root.right_child = Node("", self.t.root, 1)
                self.t.root.left_child = Node(gamma, self.t.root, 1)
            
            # Add counterexample to the dictionary
            self.update_dictionary(gamma, 1)

    ##########################################################################################################

    # Updates the access string reference dictionary with the given values
    # Isolated to its own method for debugging purposes (prevent clobbering)
    def update_dictionary(self, key : str, index : int):
        # TODO: Delete debugging print statement
        # print("adding key " + key + " to dictionary")
        
        # assert (not key in self.access_string_reference.keys()) 

        # Print debugging information if trying to clobber a pre-existing key:
        if key in self.access_string_reference.keys():
            print("trying to clobber key " + key)
            self.__sift(key)
            #exit(1)
            assert not key in self.access_string_reference.keys()

        self.access_string_reference.update({key : index})

    ##########################################################################################################

    def lstar_algorithm(self):
        print("running l-star")

        while not self.solved:
            # create new M_hat from current T => call construct_hypothesis
            self.m_hat = self.construct_hypothesis()
            # TODO: delete debugging print statements
            
            print(f"m_hat updated {self.m_hat}")

            if self.graphs:
                self.draw_graph()
                print("graph displayed.")
            
            # print("m_hat updated " + str(self.m_hat))
            # equivalence query => does our current M_hat equal the real M from teacher?
            gamma = self.my_teacher.equivalent(self.m_hat)

            # TODO: Delete debugging print statement
            # print("Counterexample is ===> " + str(gamma))
            if gamma:
                # if a counterexample is provided, update T by determining the new access string and distinguishing string (sift down)
                assert(self.my_teacher.member(gamma) != self.my_teacher.member(gamma, self.m_hat, self.alphabet))

                assert type(gamma) is str

                # call update_tree (includes updating dictionary)
                self.update_tree(gamma)

                # TODO: Delete debugging print statements
                # print("number of entries in dictionary: " + str(len(self.access_string_reference)))
                # print("number of rows in M_hat: " + str(len(self.m_hat)))

            else:
                # If no counterexample is provided, the DFA has been solved
                self.solved = True

            # TODO: Delete debugging print statement
            # print("LOOP COMPLETE IN L STAR")

        # If we have exited the loop, we have solved the DFA
        # if yes we are done
        print("DFA solved!")
        print(f"Learned DFA with {len(self.m_hat)} states:")
        print(self.m_hat)
        print("with tree:")
        self.t.print_tree()
        
        print("End L-Star algorithm")

    ##########################################################################################################

    # Finds and returns the distinguishing string corresponding to the last (most recent) common ancestor of the access strings s1 and s2 in T
    def __get_lca(self, s1 , s2):
        # Get the tree nodes corresponding to the two passed access strings
        # NOTE: We could also have passed n1 instead of s1 to this method, but we would need to sift for s2 (which comes from M_hat) regardless
        n1 = self.__sift_return_node(s1)
        n2 = self.__sift_return_node(s2)

        # Travel up the tree until you've found the point in n1 and n2's family trees when they are on the same level
        while n1.level > n2.level:
            n1 = n1.parent
        
        while n2.level > n1.level:
            n2 = n2.parent
        
        assert n1 and n2
        assert n1.level == n2.level

        # Travel up the family trees until you are looking at the same node via both paths
        while n1 != n2:
            n1 = n1.parent
            n2 = n2.parent

            assert n1 and n2
        
        # Confirm that we have found a common ancestor
        assert n1 == n2

        # Return the distinguishing string assosciated with the LCA
        return n1.value
    
    ##########################################################################################################

    # input: gamma (a counterexample generated from an equivalence query) and our tree T (from self)
    # output: Edits T to update it (returns nothing)
    # NOTE: remember to SET THE PARENT of a new node when you declare it
    def update_tree(self, gamma):
        # TODO: Delete debugging print statements
        # print("Update tree called")
        # print(f"Updating the tree with {gamma}")

        # Assert that gamma really is a counterexample
        assert bool(self.my_teacher.member(gamma)) != bool(self.my_teacher.member(gamma, self.m_hat, self.alphabet))


        j = 0
        mismatch_found = False
        # for each prefix set of characters of gamma
        for i in range(len(gamma)):
            j = i

            # Get the first i characters of gamma
            strng = gamma[0 : i + 1]
            # sift gamma[i] in T
            node_sift = self.__sift_return_node(strng)
            access_string_sift = node_sift.value
            loop_d = node_sift.parent.value if node_sift.parent else ""

            # Accessing dictionary key from value according to these instructions: https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/#
            # TODO: This is a janky way to be using a dictionary. Is this the best-suited ADT for our purposes?
            row_in_m_hat = self.m_hat.index(Teacher.final_state(strng, self.m_hat, self.alphabet))
            my_dict = self.access_string_reference
            access_string_m_hat = list(my_dict.keys())[list(my_dict.values()).index(row_in_m_hat)]
            
            # Repeat loop until sifting and running the truncated string through M_hat lead to distinct states (different access strings/row indices in M_hat)
            #if self.access_string_reference[access_string] != self.m_hat.index(Teacher.final_state(strng, self.m_hat, self.alphabet)):
            if access_string_sift != access_string_m_hat:
                # TODO: Delete debugging print statements
                # print(f"strng {strng}")
                # print(f"Access string from sifting: {access_string_sift if access_string_sift else "empty string"}")
                # print(f"Access string from M_hat: {access_string_m_hat if access_string_m_hat else "empty string"}")
                # print("breaking loop")
                mismatch_found = True
                break
        
        # Assert that we haven't left the loop just because of iterating through all values of i
        assert mismatch_found

        # Find the last common ancestor (lca) of access_string_sift and access_string_m_hat in T
        lca = self.__get_lca(access_string_sift, access_string_m_hat)

        # let j be the least i such that s[i] does not equal s_hat[i]
        gamma_j_minus_1 = gamma[0 : j]
        # TODO: Delete debugging print statement
        #print(f"gamma[j-1]: {gamma_j_minus_1}, j = {j}")

        # Update dictionary with access string
        assert(gamma_j_minus_1 != "")
        self.update_dictionary(gamma_j_minus_1, len(self.access_string_reference))
        
        # Get node in tree T to edit
        node_to_edit = self.__sift_return_node(gamma_j_minus_1)
        s_j_minus_1 = node_to_edit.value
    
        # The new distinguishing string is the character gamma[j] concatonated with
        # the last common ancestor distinguishing string between access_string_sift and access_string_m_hat in T
        new_d = gamma[j] + lca


        assert new_d
        assert self.my_teacher.member(s_j_minus_1 + new_d) != self.my_teacher.member(gamma_j_minus_1 + new_d)

        # TODO: Delete debugging print statements
        # print(f"node to edit value: {node_to_edit.value}")
        # print(f"node to edit parent value: {(node_to_edit.parent.value if node_to_edit.parent.value else "empty") if node_to_edit.parent else "no parent"}")
        # print(f"new distinguishing string: {new_d}")
        # print(f"s[j-1] = {s_j_minus_1}")
        # print(f"gamma[j-1] = {gamma_j_minus_1}")

        # self.t.print_tree()
        # print(self.m_hat)


    
        # Create child leaves for node_to_edit, making it an internal node
        assert (not node_to_edit.left_child) and (not node_to_edit.right_child)
        node_to_edit.left_child = Node(None, node_to_edit, node_to_edit.level + 1)
        node_to_edit.right_child = Node(None, node_to_edit, node_to_edit.level + 1)
    
        # Set values of node_to_edit's children
        # leaf nodes are the previous access string and the new access string gamma[j-1]
        # Determine which leaf node goes on each side by checking membership when concatenated with the new distinguishing string        
        if self.my_teacher.member(s_j_minus_1 + new_d) and not self.my_teacher.member(gamma_j_minus_1 + new_d):
            node_to_edit.right_child.value =  s_j_minus_1
            node_to_edit.left_child.value = gamma_j_minus_1
        elif self.my_teacher.member(gamma_j_minus_1 + new_d) and not self.my_teacher.member(s_j_minus_1 + new_d):
            node_to_edit.right_child.value = gamma_j_minus_1
            node_to_edit.left_child.value =  s_j_minus_1
        else:
            print(f"Both {s_j_minus_1 + new_d} and {gamma_j_minus_1 + new_d} are {"accepted" if self.my_teacher.member(s_j_minus_1 + new_d) else "rejected"}")
            exit(f"Error: Unable to sort access string {gamma_j_minus_1} into T")

        # Set node_to_edit's value to be the new distinguishing string
        assert node_to_edit.parent
        node_to_edit.value = new_d

        # TODO: Delete debugging print statement
        # print("update tree done.")

    ##########################################################################################################

    # input: T is our classification tree
    # output: hypothesis M_hat constructed from T
    def construct_hypothesis(self):
        # TODO: Delete debugging print statement
        # print("construct hypothesis called")
        to_become = []

        # for each access string (leaf) of T, create a state in M_hat
        for key in self.access_string_reference.keys():
            to_append = []
            
            # Save a boolean indicating if the given key corresponds to an accept or reject state
            if self.my_teacher.member(key):
                to_append.append(1)
            else:
                to_append.append(0)

            # Create space for the arrows
            for i in range(len(self.alphabet)):
                to_append.append(-1)
            
            # TODO: Delete debugging print statements
            # print(f"appending row to to_become for key {key}")
            to_become.append(to_append)
        
        #print("M_hat mid-construction: " + str(to_become))

        #print("access_string_reference.keys(): " + str(self.access_string_reference.keys()))

        # start state of M_hat is lambda, the empty string
        # for each state in M_hat and each symbol b in the language, compute the b-transition out of the access string s:
        for key in self.access_string_reference.keys():
            # for each symbol b in the language, sift
            for b in self.alphabet:
                resulting_state = self.__sift(key + b)
                # direct the b-transition out of s to the resulting sifted state in M_hat
                to_direct = self.access_string_reference[resulting_state]
                # set TO BECOME [ index of key string ] [ index of character b in alphabet ] to be equal to to_direct
                # TODO: Delete debugging print statements
                #print("dictionary: " + str(self.access_string_reference))
                #print("key: " + key)
                #print("row index: " + str(self.access_string_reference[key]))
                #print("rows in to_become: " + str(len(to_become)))
                to_become[self.access_string_reference[key]][self.alphabet.index(b) + 1] = to_direct

        # Ensure that all -1s have been overwritten
        for row in to_become:
            for entry in row:
                assert entry >= 0

        # TODO: Delete debugging print statements
        # print("new m_hat:")
        # print(to_become)
        return to_become

    ##########################################################################################################

    # input: s is the string being sifted and T is our tree
    # output: leaf NODE (not access string) in T for the state of M accessed by s
    def __sift_return_node(self, s):
        # TODO: Delete debugging print statement
        # print("sift_return_node called on " + (s if s else "the empty string"))
        
        # set current node to root of T
        current = self.t.root

        loops_to_find_leaf = 0

        # Loop as long as current has a left child (that is, as long as current is not a leaf)
        while (current.left_child):
                        
            # d is distinguishing string at current node
            d = current.value

            #print("current.value: " + d)
            #print(s + " + " + d + " is " + ("accepted" if self.my_teacher.member(s+d) else "rejected") + " by M")

            # membership query on sd (concatenated) 
            # if membership query is accepted, current node is right child of current node
            if self.my_teacher.member(s + d):
                current = current.right_child
            # else (if rejected), current node is left child of current node
            else:
                current = current.left_child
            
            loops_to_find_leaf += 1
                    
        # NOTE: We have reached this point because current does not have a left child.
        # Because each tree node should have either 0 or 2 children (not 1), this means that current should also not have a right child
        assert not current.right_child

        #print("loops to find leaf: " + str(loops_to_find_leaf))

        # Check that access string is properly stored
        assert (current.value in self.access_string_reference.keys())
        
        # Return the access string at the leaf found
        # TODO: Delete debugging print statement
        # print(f"ending sift after {loops_to_find_leaf} loops. returning NODE {self.access_string_reference[current.value]} with access string {current.value if current.value else "empty"}")
        return current

    ##########################################################################################################

    # input: s is the string being sifted and T is our tree
    # output: access string in T for the state of M accessed by s
    def __sift(self, s):
        #print("---")
        #print("sift called on " + (s if s else "the empty string"))
        return self.__sift_return_node(s).value
    
    ##########################################################################################################

##############################################################################################################

class Node:

    ##########################################################################################################

    def __init__(self, value : str, parent, level):
        self.value = value

        self.parent = parent

        # always have 0 or 2 children, never only 1 child, due to distinguishing string logistics
        self.left_child = None
        self.right_child = None
        
        # The level of the tree at which the node is located (root = 0)
        self.level = level
    
    ##########################################################################################################

##############################################################################################################

class Tree:

    ##########################################################################################################

    def __init__(self, root: Node):
        self.root = root

    ##########################################################################################################

    # other methods go here ie sorting stuff
    def print_tree(self):
        stack = []
        stack.append(self.root)
        while stack:
            to_print = stack.pop()
            # append right child first so the left child gets printed first
            if to_print.right_child is not None:
                stack.append(to_print.right_child)
            if to_print.left_child is not None:
                stack.append(to_print.left_child)
            
            n = to_print
            while n.parent is not None:
                print("\t", end="")
                n = n.parent
            
            # Specify if the string is a distinguishing string or access string
            # If the string is empty, print "empty." If it is NoneType, indicate lack of initialization. If it has a non-empty value, print it
            # Also print the level at which the node is located
            print(f"{"d" if to_print.left_child else "s"}: {("empty" if to_print.value == "" else to_print.value) if (to_print.value != None) else "not initialized"}, level {to_print.level}")

    ##########################################################################################################

##############################################################################################################