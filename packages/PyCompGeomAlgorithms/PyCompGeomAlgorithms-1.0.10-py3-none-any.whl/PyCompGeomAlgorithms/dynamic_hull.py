from copy import deepcopy
from enum import Enum
from .core import BinTreeNode, AVLTree, ThreadedBinTree, ThreadedBinTreeNode, PointType, Point
from .jarvis import jarvis


class DynamicHullNode(BinTreeNode):
    def __init__(self, data, subhull=None, left_supporting_index=0):
        super().__init__(data)
        self.subhull = subhull
        self.left_supporting_index = left_supporting_index
    
    @property
    def point(self):
        return self.data
    
    @point.setter
    def point(self, value):
        self.data = value
    
    @point.deleter
    def point(self):
        del self.data

    @property
    def is_point(self):
        return self.subhull.root.is_leaf

    @property
    def is_segment(self):
        root = self.subhull.root
        return not root.left and root.right and root.right.is_leaf
    
    @classmethod
    def leaf(cls, point):
        return cls(point, SubHullThreadedBinTree.from_iterable([point]))

    def __eq__(self, other):
        return (
            super().__eq__(other)
            and self.subhull == other.subhull
            and self.left_supporting_index == other.left_supporting_index
        )
    
    def __repr__(self):
        return ", ".join(repr(node.point) for node in self.subhull.traverse_inorder())


class DynamicHullTree(AVLTree):
    node_class = DynamicHullNode

    @classmethod
    def from_iterable(cls, iterable):
        return cls(cls._from_iterable(iterable))
    
    @classmethod
    def _from_iterable(cls, iterable, i=None, n=None):
        if i is None:
            i = [0]
        if n is None:
            n = len(iterable)
        if n == 1:
            res = DynamicHullNode(iterable[i[0]], SubHullThreadedBinTree.from_iterable([iterable[i[0]]]))
            i[0] += 1
            return res

        n_right = n // 2
        n_left = n - n_right
        left, right = cls._from_iterable(iterable, i, n_left), cls._from_iterable(iterable, i, n_right)
        node = merge(left, right)

        return node
    
    def insert(self, point, starting_node=None, path=None):
        if starting_node is None:
            starting_node = self.root
        if path is None:
            path = []
        
        self.root = self._insert(point, starting_node, path)
    
    def _insert(self, point, node, path):
        if node.is_leaf:
            node_copy = deepcopy(node)
            new_node = DynamicHullNode.leaf(point)
            node.left = new_node if point < node.point else node_copy
            node.right = node_copy if point < node.point else new_node
        elif point < node.point:
            path.append(PathDirection.left)
            node.left = self._insert(point, node.left, path)
        else:
            path.append(PathDirection.right)
            node.right = self._insert(point, node.right, path)

        return self._merge_with_rebalance(node)
    
    def delete(self, point, starting_node=None, path=None):
        if starting_node is None:
            starting_node = self.root
        if path is None:
            path = []
        
        self.root = self._delete(point, starting_node, path)
    
    def _delete(self, point, node, path):
        if node.is_leaf:
            return None
        elif point <= node.point:
            path.append(PathDirection.left)
            node.left = self._delete(point, node.left, path)
        else:
            path.append(PathDirection.right)
            node.right = self._delete(point, node.right, path)
        
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        
        return self._merge_with_rebalance(node)
    
    def _merge_with_rebalance(self, node):
        node.set_height()

        if node.balance_factor == -2 or node.balance_factor == 2:
            bf, left_bf, right_bf = node.balance_factor, node.left.balance_factor, node.right.balance_factor
            node = self.rebalance(node)

            # Re-evaluate lower subhulls affected by rebalancing
            if (bf == 2) or (bf == -2 and left_bf == 1):
                node.left = merge(node.left.left, node.left.right)
            if (bf == -2) or (bf == 2 and right_bf == -1):
                node.right = merge(node.right.left, node.right.right)

        return merge(node.left, node.right)


class SubHullNode(ThreadedBinTreeNode):
    @property
    def point(self):
        return self.data
    
    @point.setter
    def point(self, value):
        self.data = value
    
    @point.deleter
    def point(self):
        del self.data


class SubHullThreadedBinTree(ThreadedBinTree):
    node_class = SubHullNode

    @classmethod
    def from_iterable(cls, iterable, circular=False):
        return super().from_iterable(iterable, circular)


class PathDirection(Enum):
    left = "left"
    right = "right"


def upper_dynamic_hull(points, point_to_insert_or_delete):
    points.sort()
    
    tree = DynamicHullTree.from_iterable(points)
    yield tree.leaves_inorder()
    yield tree
    yield tree
    yield tree
    yield tree

    optimized_tree = deepcopy(tree)
    optimize_dynamic_hull_tree(optimized_tree.root)
    yield optimized_tree

    path = []
    if point_to_insert_or_delete in points:
        tree.delete(point_to_insert_or_delete, path=path)
    else:
        tree.insert(point_to_insert_or_delete, path=path)
    
    yield path

    optimize_dynamic_hull_tree(tree.root)
    hull = [n.point for n in tree.root.subhull.traverse_inorder()]

    yield tree, hull
    yield hull


def merge(node1, node2):
    if node1.is_point or node2.is_point or node1.is_segment or node2.is_segment:
        return merge_trivial(node1, node2)

    subhull_node1, subhull_node2 = node1.subhull.root, node2.subhull.root
    prev1, prev2 = None, None
    while prev1 != subhull_node1 or prev2 != subhull_node2:
        prev1, prev2 = subhull_node1, subhull_node2
        subhull_node1, subhull_node2 = next_nodes(subhull_node1, subhull_node2)
    
    subhull_nodes1, subhull_nodes2 = node1.subhull.traverse_inorder(), node2.subhull.traverse_inorder()
    subhull = [
        node.point for node in
        subhull_nodes1[:subhull_nodes1.index(prev1)+1] + subhull_nodes2[subhull_nodes2.index(prev2):]
    ]
    
    joint_node = DynamicHullNode(
        data=node1.rightmost_node.point,
        subhull=SubHullThreadedBinTree.from_iterable(subhull),
        left_supporting_index=subhull.index(prev1.point)
    )
    joint_node.left, joint_node.right = node1, node2
    joint_node.set_height()
    
    return joint_node


def merge_trivial(node1, node2):
    """
        Merge two nodes by constructing the convex hull of their points with Jarvis' algorithm and extracting its upper part.
        
        For efficiency's sake, only use in trivial cases, such as point & point, segment & point, segment & segment, and segment & 3-chain.
    """
    subhull_root1, subhull_root2 = node1.subhull.root, node2.subhull.root
    points1 = [node.point for node in subhull_root1.traverse_inorder()]
    points2 = [node.point for node in subhull_root2.traverse_inorder()]
    points = points1 + points2
    subhull = (
        ([] if len(points) == 2 and points[0].x == points[1].x else [points[0]]) +
        [p for p in jarvis(points) if Point.direction(points[0], points[-1], p) < 0] +
        [points[-1]]
    )
    
    rightmost_point_in_left_subtree = node1.rightmost_node.point
    left_supporting_point = subhull[0] if len(subhull) == 1 else next(p for p in reversed(points1) if p in subhull)
    joint_node = DynamicHullNode(
        data=rightmost_point_in_left_subtree,
        subhull=SubHullThreadedBinTree.from_iterable(subhull),
        left_supporting_index=subhull.index(left_supporting_point)
    )
    joint_node.left, joint_node.right = node1, node2
    joint_node.set_height()

    return joint_node


def next_nodes(node1, node2):
    type1, type2 = PointType.by_nodes(node2, node1), PointType.by_nodes(node1, node2)
    return next_left_node(node1, type1), next_right_node(node2, type2)


def next_left_node(node, point_type):
    return {
        PointType.reflex: node.right,
        PointType.right_supporting: node,
        PointType.convex: node.left
    }[point_type]


def next_right_node(node, point_type):
    return {
        PointType.reflex: node.left,
        PointType.left_supporting: node,
        PointType.convex: node.right
    }[point_type]


def optimize_dynamic_hull_tree(node, parent_node=None):
    if node.left:
        optimize_dynamic_hull_tree(node.left, node)
    if node.right:
        optimize_dynamic_hull_tree(node.right, node)
    if parent_node:
        optimize_subhull(node, parent_node)


def optimize_subhull(node, parent_node):
    node_points = [n.point for n in node.subhull.traverse_inorder()]
    parent_points = {n.point for n in parent_node.subhull.traverse_inorder()}

    filtered_points = [p for p in node_points if p not in parent_points]
    node.subhull = SubHullThreadedBinTree.from_iterable(filtered_points)
