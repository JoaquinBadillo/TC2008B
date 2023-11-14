import math
import argparse
from functools import reduce

class Node:
    def __init__(self, x, y, z):        
        self.coords = (x, y, z)

    # Inner Product
    def dot(self, node):
        return reduce(
            lambda x, y: x + y[0] * y[1],
            zip(self.coords, node.coords),
            0
        )

    # Normalized Cross Product
    def cross(self, node: 'Node'):        
        mag = math.sqrt(node.dot(node)) * math.sqrt(self.dot(self))

        return Node(
            (self.coords[1] * node.coords[2] - self.coords[2] * node.coords[1]) / mag,
            (self.coords[2] * node.coords[0] - self.coords[0] * node.coords[2]) / mag,
            (self.coords[0] * node.coords[1] - self.coords[1] * node.coords[0]) / mag
        )

    # Magnitude
    def __abs__(self):
        return math.sqrt(self.dot(self.coords))
    
    # (Normalized) Cross Product
    def __mul__(self, node):
        return self.cross(node)
    
    # Vector Subtraction
    def __sub__(self, node):
        x, y, z = tuple((comp - node.coords[i] for i, comp in enumerate(self.coords)))
        return Node(x, y, z)
    
    # Writing to file
    def __str__(self):
        return " ".join(f"{x:.16f}" for x in self.coords)

class Triangle:
    def __init__(self, nodes, normal):
        self.nodes = tuple(node for node in nodes)
        self.normal = normal
    
    def __str__(self):
        return " ".join(tuple(f"{point}//{self.normal}" for point in self.nodes))
     
def angle(i, n):
    return 2 * math.pi * i / n
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--nodes', nargs='?', default = 20, dest='n', type=int, help="Number of nodes for a circle")
    parser.add_argument('--radius', nargs='?', default = 1, dest='r', type=int, help="Circle radius")
    parser.add_argument('--depth', nargs='?', default = 1, dest='d', type=int, help="Depth")
    args = parser.parse_args()
    
    numNodes = args.n
    radius = args.r
    depth = args.d

    nodes = [
        Node(depth / 2, 0, 0), 
        Node(-depth / 2, 0, 0)
    ]

    normals = [
        Node(1, 0, 0),
        Node(-1, 0, 0)
    ]

    faces = []

    currentNode = 2
    currentNormal = 2

    ang = angle(-1, numNodes)
    x = depth / 2

    y = radius * math.sin(ang)
    z = radius * math.cos(ang)

    memo = [
        [Node(x, y, z), 2 * numNodes - 1],
        [Node(-x, y, z), 2 * numNodes]
    ]

    for i in range(numNodes + 1):
        ang = angle(i, numNodes)
        
        y = radius * math.sin(ang)
        z = radius * math.cos(ang)

        nodes.append(Node(x, y, z))
        currentNode += 1

        # Front
        faces.append(
            Triangle(
                [1, currentNode, memo[0][1]],
                1
            )
        )

        nodes.append(Node(-x, y, z))
        currentNode += 1

        # Back
        faces.append(
            Triangle(
                [2, memo[1][1], currentNode],
                2
            )
        )

        # Normals:
        n1 = memo[1][0] - memo[0][0]
        n2 = nodes[currentNode - 2] - memo[0][0]

        normals.append(n1 * n2)
        currentNormal += 1

        # Side T1
        faces.append(
            Triangle(
                [memo[0][1], currentNode - 1, currentNode],
                currentNormal
            )
        )

        # Side T2
        faces.append(
            Triangle(
                [currentNode, memo[1][1], memo[0][1]],
                currentNormal
            )
        )

        memo[0] = [nodes[currentNode - 2], currentNode - 1]
        memo[1] = [nodes[currentNode - 1], currentNode]


    # Dump Results to file

    with open("wheel.obj", "w") as f:
        f.write("# Wheel\n")

        for node in nodes:
            f.write(f"v {node}\n")

        for normal in normals:
            f.write(f"vn {normal}\n")

        for face in faces:
            f.write(f"f {face}\n")