from tkinter import *
import tkinter as tk
import tkinter.messagebox
import customtkinter
from code import *
from PIL import Image, ImageTk
import webbrowser

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1280}x{720}")
        self.resizable(False,False)
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="PATHFINDING\nVISUALIZER", font=("Helvetica", 20, "bold"),text_color="#f1faee")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,text="About Algorithms", command=self.sidebar_about_button,fg_color="#2B2A2A")
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame,text="Working", command=self.sidebar_working_button,fg_color="#2B2A2A")
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame,text="About Code", command=self.sidebar_code_button,fg_color="#2B2A2A")
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame,text="Learn More" ,command=self.sidebar_learn_button,fg_color="#2B2A2A")
        self.sidebar_button_4.grid(row=5 ,column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["System","Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_optionemenu.set(value="System")
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=11, column=0, padx=20, pady=(10, 0))
        self.option_menu1 = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.option_menu1.set(value="100%")
        self.option_menu1.grid(row=12, column=0, padx=20, pady=(10, 20))


        self.about_frame=customtkinter.CTkFrame(self,height=200, width=200) 
        self.about_frame.grid(row=0, column=1,padx=15, pady=15, rowspan=20, sticky="nsew")
        self.about_frame.place()
        self.sidebar_frame.grid_rowconfigure(100, weight=1)


        self.main_frame_label=customtkinter.CTkLabel(self.about_frame, text="Please choose a topic to Start Learning.", font=("Helvetica", 40,"bold"))
        self.main_frame_label.pack(pady=300,side="top")
        self.main_frame_label2=customtkinter.CTkLabel(self.about_frame, text="To learn these topics in more detail, please visit our website.", font=("Helvetica", 20,"bold"))
        self.main_frame_label2.pack(side="top")
    
        

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_about_button(self):
        for widget in self.about_frame.winfo_children():
            widget.destroy()
            self.sidebar_button_2.configure(fg_color="#2B2A2A")
            self.sidebar_button_3.configure(fg_color="#2B2A2A")
            self.sidebar_button_4.configure(fg_color="#2B2A2A")

        self.color=self.sidebar_button_1.configure(fg_color="green")

        self.textbox = customtkinter.CTkTextbox(self.about_frame,font=("Helvetica", 18), width=1050, height=670)
        self.textbox.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="W")
        self.textbox.insert(index="1.0",text="This section includes basic explanation of 6 Algorithms:\n\n1. Breadth-First Search Algorithm\n\n2. Depth-First Search Algorithm\n\n"
        "3.Dijkstra's Algorithm\n\n4. A* (A-Star) Algorithm\n\n5. Floyd-Warshal Algorithm\n\n6. Swarm Intelligence Algorithm\n\nIf you need more detailed explanation of all these"
        " algorithm please visit our website\t\t.thankyou\n\n\n\n"
"BREADTH-FIRST SEARCH:\n\n""  i. The breadth-first search(BFS) algorithm is used to search a tree or graph data structure for a node that meets a set of criteria.\n\n"
"ii. It is a recursive algorithm to search all the vertices of a tree or graph data structure.\n\n"
"iii. Breadth-first search is a graph traversal algorithm that starts traversing the graph from the root node and explores all the neighbouring nodes.\n\n"
"iv. Then, it selects the nearest node and explores all the unexplored nodes. While using BFS for traversal, any node in the graph can be considered\n"
"      as the root node.\n\n"
"v. BFS puts every vertex of the graph into two categories: visited and non-visited. It selects a single node in a graph and, after that, visits all the nodes\n"
"      adjacent to the selected node.\n\n"
"vi. The data structure used in BFS is Queue.\n\n" 
"vii. Time complexity of BFS is O(V+E) and space complexity of BFS is O(V).\n\n\n\n"
"DEPTH-FIRST SEARCH:\n\n"
"i. Depth-first search or depth-first traversal is a recursive algorithm for searching all the vertices of a graph or a tree data structure.\n\n"
"ii. The depth-first search(DFS) algorithm starts with the initial node of Graph G and goes deeper until we find the goal node or the node with no children\n\n"
"iii. Because of the recursive nature, stack data structure can be used to implement the DFS algorithm. \n\n"
"iv. The data structure used in DFS is Stack.\n\n"
"v. Time complexity of DFS is O(V+E) and space complexity of DFS is O(V).\n\n\n\n" 
"DIJKSTRA'S ALGORITHM:\n\n"
"i. Dijkstra’s algorithm is an algorithm for finding the shortest paths between nodes in a graph, which may represent, for example, road networks.\n"    
"    It was conceived by computer scientist Edsger W. Dijkstra in 1956 and published three years later.\n\n"
"ii. Dijkstra’s original algorithm found the shortest path between two given nodes, but a more common variant fixes a single node as the “source” \n"
"     node and finds shortest paths from the source to all other nodes in the graph, producing a shortest-path tree.\n\n"
"iii. For a given source node in the graph, the algorithm finds the shortest path between that node and every other. It can also be used for finding \n"
"     theshortest paths from a single node to a single destination node by stopping the algorithm once the shortest path to the destination node has\n"
"     been determined.\n\n"
"v. For example, if the nodes of the graph represent the cities and costs of edge paths represent driving distances between pairs of cities connected \n"
"     by a direct road(for simplicity, ignore red lights, stop signs, toll roads and other obstructions), then Dijkstra’s algorithm can be used to \n"
"     find the shortest route between one city and all other cities.\n\n"
"v. A widely used application of shortest path algorithms is network routing protocols, most probably IS-IS(Intermediate System to Intermediate  \n"
"     System) and OSPF(Open Shortest Path First).\n\n"
"vi. The Dijkstra algorithm uses labels that are positive integers or real numbers, which are totally ordered. It can be generalized to use any \n"
"     labels that arepartially ordered, provided the subsequent labels are monotonically non-decreasing. This generalization is called the generic \n"
"     Dijkstra shortest-path algorithm.\n\n\n\n"
"A* (A-Star) ALGORITHM:\n\n"
"i. A* search is the most commonly known form of best-first search.\n\n"
"ii. It uses heuristic function h(n), and cost to reach the node n from the start state g(n). \n\n"
"iii. It has combined features of Unified Computing System(UCS) and greedy best-first search, by which it solves the problem efficiently.\n\n"
"iv. A* search algorithm finds the shortest path through the search space using the heuristic function. This search algorithm expands less search\n"
"     tree and provides optimal result faster. \n\n"
"v. A* algorithm is like Unified Computing System(UCS) except  that is used g(n)+h(n) instead of g(n).\n\n"
"vi. In A* search algorithm, we use search heuristic as well as the cost to reach the node. Hence, we can combine both costs as following, and \n\n"
"     this sum is called as the fitness number.\n"
"\t\t\t\t\t\tf(n)=g(n)+h(n)\n\n\n\n\n"
"FLOYD-WARSHALL ALGORITHM:\n\n"
"i. Floyd-Warshall Algorithm is an algorithm for finding the shortest path between all the pairs of vertices in a weighted graph. \n\n"
"ii. This algorithm works for both the directed and undirected weighted graphs. But, it does not work for the graphs with negative cycles(where\n"
"     the sum of the edges in a cycle is negative).\n\n"
"iii. This algorithm follows the dynamic programming approach to find the shortest path. \n\n"
"iv. There are three loops. Each loop has constant complexities. So, the time complexity of the Floyd-Warshall algorithm is O(n3).\n\n"
"v. The space complexity of the Floyd-Warshall algorithm is O(n2).\n\n\n\n"
"SWARM INTELLIGENCE ALGORITHM:\n\n"
"i. Swarm Intelligence(S.I.) algorithm was introduced by Gerardo Beni and Jing Wang in the year 1989. S.I. simply means using the knowledge\n"
"    of collective objects(people, collects, etc.) together and then reaching the optimized solution for a given problem.\n\n"
"ii. “Swarm” means a group of objects(people, insects, etc.). In other words, let’s say we give a problem statement to a single person and \n"
"    tell him or her to go through this problem and then give the solution, then this means that we will consider the solution of that particular\n"
"    person only, but the problem is that the solution given by that person may not be the best solution or maybe, that solution is not good for others.\n\n"
"iii. So, to avoid that, what we do is we give that problem to a certain amount of people together(swarm) and ask them to reach the best solution\n"
"    possible for that problem, and then computing all the responses together to reach the best solution possible, so here we are using the \n"
"    knowledge of the group as a whole to reach the best solution or optimized solution for that problem and that solution will be good for all of \n"
"    them individually too, so that is the idea behind Swarm Intelligence Algorithm.\n\n")
        self.textbox.configure(state="disabled")
 

    def sidebar_working_button(self):
        for widget in self.about_frame.winfo_children():
            widget.destroy()
            self.sidebar_button_1.configure(fg_color="#2B2A2A")
            self.sidebar_button_3.configure(fg_color="#2B2A2A")
            self.sidebar_button_4.configure(fg_color="#2B2A2A")

        self.color=self.sidebar_button_2.configure(fg_color="green")

        self.textbox = customtkinter.CTkTextbox(self.about_frame,font=("Helvetica", 20), width=1050, height=670)
        self.textbox.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="W")
        self.textbox.insert(index="1.0",text="Breadth-First Search (BFS) works by exploring all the neighboring nodes of a source node before moving on to the next layer of nodes. It uses a queue to keep track of the nodes to be visited next, adding the neighbors of a node to the queue before visiting the next node in the queue. BFS finds the shortest path in an unweighted graph or a graph where all edges have the same weight.\n\n"
"Depth-First Search (DFS) works by exploring the graph as far as possible along each branch before backtracking. It uses a stack to keep track of the nodes to be visited next, visiting the deepest node first before backtracking to its neighbors. DFS can be used to find all the paths from a source node to a target node.\n\n"
"A* (A-star) algorithm is a variant of Dijkstra's algorithm that uses a heuristic function to estimate the remaining cost to the target node. The heuristic function guides the search by prioritizing the nodes that are estimated to be closer to the target node. A* is more efficient for finding a single target path and is often used in navigation and game AI.\n\n"
"Dijkstra's algorithm finds the shortest path from a source node to all other nodes in a weighted graph, where the edge weights represent distances or costs. It uses a priority queue to keep track of the nodes to be visited next, visiting the node with the lowest cost first. Dijkstra's algorithm can be used to find the shortest path between two nodes or to precompute the shortest paths from a source node to all other nodes.\n\n"
"In summary, BFS is useful for finding the shortest path in an unweighted graph, DFS can be used to find all paths from a source to a target, A* is efficient for finding a single target path, and Dijkstra's algorithm finds the shortest path in a weighted graph.\n\n\n\n"
"Here are the time and space complexities for each algorithm:\n\n"
"Breadth-First Search (BFS):\n\n"
"Time complexity: O(|V| + |E|), where |V| is the number of nodes and |E| is the number of edges in the graph.\n\n"
"Space complexity: O(|V|), as the queue used to keep track of the nodes to be visited next can store all the nodes in the worst case.\n\n\n\n"
"Depth-First Search (DFS):\n\n"
"Time complexity: O(|V| + |E|), where |V| is the number of nodes and |E| is the number of edges in the graph.\n\n"
"Space complexity: O(|V|), as the stack used to keep track of the nodes to be visited next can store all the nodes in the worst case.\n\n\n\n"
"A* (A-star) algorithm:\n\n"
"Time complexity: O(|E| + |V| * log |V|), where |V| is the number of nodes and |E| is the number of edges in the graph. This assumes that the heuristic function is admissible (never overestimates the cost to the target) and consistent (the cost from node A to node B is less than or equal to the sum of the costs from A to C and C to B).\n\n"
"Space complexity: O(|V|), as the priority queue used to keep track of the nodes to be visited next can store all the nodes in the worst case.\n\n\n\n"
"Dijkstra's algorithm:\n\n"
"Time complexity: O(|E| + |V| * log |V|), where |V| is the number of nodes and |E| is the number of edges in the graph.\n\n"
"Space complexity: O(|V|), as the priority queue used to keep track of the nodes to be visited next can store all the nodes in the worst case.\n\n"
"Note: In practice, the actual running time of these algorithms can be influenced by the implementation and the structure of the graph, such as the number of edges per node and the distribution of edge weights.\n")
        self.textbox.configure(state="disabled")

    
    def sidebar_code_button(self):
        for widget in self.about_frame.winfo_children():
            widget.destroy()
            self.sidebar_button_1.configure(fg_color="#2B2A2A")
            self.sidebar_button_2.configure(fg_color="#2B2A2A")
            self.sidebar_button_4.configure(fg_color="#2B2A2A")

        self.color=self.sidebar_button_3.configure(fg_color="green")
        self.textbox = customtkinter.CTkTextbox(self.about_frame,font=("Helvetica", 20), width=1050, height=670)
        self.textbox.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="W")
        self.textbox.insert(index="1.0",text="To create the visualizer, you likely started by using Tkinter to create a graphical user interface (GUI) for the user to interact with. This may have involved creating a grid to represent the graph, and allowing the user to place obstacles or walls on the grid by clicking on the individual cells. The user may also have the ability to select the source and target nodes by clicking on the cells representing these nodes.\n\n"
"You then implemented the four algorithms (BFS, DFS, A*, and Dijkstra's) to find a path from the source node to the target node. Each algorithm may have been implemented as a separate function that takes in the graph as an input and returns the path as an output.\n\n"
"For example, the BFS algorithm may have been implemented as a queue-based search that explores the graph by visiting all the neighbors of the current node before moving on to the next node. The DFS algorithm may have been implemented as a stack-based search that explores the graph by visiting a node and its neighbors before backtracking to the previous node.\n\n"
"The A* algorithm is a heuristic search algorithm that finds the shortest path between two nodes based on the estimated cost to reach the target node. The heuristic function may have been implemented using the Manhattan distance or Euclidean distance between the current node and the target node. The Dijkstra's algorithm is a greedy algorithm that finds the shortest path between two nodes by visiting nodes with the lowest cost first.\n\n"
"To visualize the pathfinding process, you likely used Tkinter to animate the search, highlighting the nodes that are being explored and the path that is being found. You may have used different colors to represent the different states of the nodes, such as visited, unexplored, and on the path. The animation may have been implemented by updating the GUI after each step of the search, giving the user a clear understanding of how the algorithm is working.\n\n"
"In summary, you created a pathfinding algorithm visualizer that uses Tkinter to create a GUI for the user to interact with, and implements the four algorithms (BFS, DFS, A*, and Dijkstra's) to find a path from a source node to a target node. The algorithms are implemented as separate functions that take in the graph as input and return the path as output. The pathfinding process is visualized using Tkinter animations, giving the user a clear understanding of how the algorithms work and the path being found.")
        self.textbox.configure(state="disabled")


    def sidebar_learn_button(self):
        for widget in self.about_frame.winfo_children():
            widget.destroy()
            self.sidebar_button_1.configure(fg_color="#2B2A2A")
            self.sidebar_button_2.configure(fg_color="#2B2A2A")
            self.sidebar_button_3.configure(fg_color="#2B2A2A")

        def open_website():
          webbrowser.open("https://www.google.com")
          self.label=customtkinter.CTkLabel(frame, text="Thankyou for Checking Out!! \nPlease Leave a Feedback :>",font=("Helvetica", 20, "bold"), text_color="black")
          self.label.pack(side="left",padx=50,pady=0)

          

        def change_color():
         colors = ["#fcf6bd", "#d0f4de", "#a9def9", "#e4c1f9", "#ff99c8","#ade8f4","#e5989b"]
         current_color = frame.cget("background")
         current_index = colors.index(current_color)
         next_index = (current_index + 1) % len(colors)
         next_color = colors[next_index]
         frame.config(background=next_color)
         frame.after(1000, change_color)

        frame = tk.Frame(self.about_frame, background="#fcf6bd")
        frame.pack(fill="both")

        self.label=customtkinter.CTkLabel(frame, text="Click the link to open the website and learn about all the algorithms and the code in detail :>",font=("Helvetica", 20, "bold"),text_color="black")
        self.label.pack(side="top",pady=(50,10))

        self.label=customtkinter.CTkLabel(frame, text="Hi",font=("Helvetica",12),text_color="black")
        self.label.pack(side="top",pady=(0,90))

        
        self.button_web=customtkinter.CTkButton(frame, text="Open Website", command=open_website,font=("Helvetica", 20, "bold"), width=150, height=100, hover_color="#bb3e03")
        self.button_web.pack(side="left",padx=(450,0), pady=(100,300))

        self.label=customtkinter.CTkLabel(frame, text="Hey! How can you see me!!!!  :<",font=("Helvetica", 10, "bold"))
        self.label.pack(side="bottom",padx=(300,0),pady=100)

        

        frame.after(1000, change_color)
    
        

        




if __name__ == "__main__":
    app = App()
    app.mainloop()
