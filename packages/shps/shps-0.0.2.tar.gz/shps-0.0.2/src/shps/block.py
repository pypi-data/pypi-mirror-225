from itertools import product, count
import numpy as np
from shps import plane, child

def tie(blocks):
    pass

def block(ne, family,
          points  = None,
          elem    = None,
          radius  = 1e-8,
          nstart  = 1,
          estart  = 1,
          join    = None,
          exclude = None,
          number  = "feap"
          ): # -> nodes, elems

    child_family = family
    nn = family.n, family.n
    block_family = plane.Lagrange(3)

    exclude = set() if exclude is None else exclude

    #
    # 1. Create edge grid in natural coordinates (-1, 1)
    #
    xl, cells = grid(ne, nn)


    #
    # 2. Create internal nodes for element type
    #
    taggen = filter(lambda i: i > len(xl) or i not in xl, count(1))

    for elem in cells.values():
        ref = child.IsoparametricMap(plane.Q4, nodes={
            1: xl[elem[0]],
            2: xl[elem[nn[0]-1]],
            3: xl[elem[nn[0]+nn[1]-2]],
            4: xl[elem[-nn[0]+1]]
        })
        for loc, node in child_family.internal_nodes.items():
            tag = next(taggen)
            xl[tag] = ref.coord(node)
            elem.insert(loc-1, tag)

    if points is None:
        return xl, cells

    #
    # 3. Map grid into problem coordinates and merge
    #
    Qn = child.IsoparametricMap(block_family, nodes=points)
    taggen = filter(lambda i: i not in tags, count(nstart))

    import scipy.spatial
    nodes = join["nodes"] if join is not None else {} # points
    if join is not None:
        tree = scipy.spatial.KDTree(np.array([x for x in nodes.values()]))
    tags = np.array(list(nodes.keys()))

    rename = {}

    for loc_tag, loc_coord in xl.items():
        tag   = None
        coord = Qn.coord(loc_coord)

        if join is not None:
            neighbors = tree.query_ball_point(coord, radius)
            if neighbors:
                tag = tags[neighbors[0]]

        if tag is None:
            tag = next(taggen)
            nodes[tag] = coord

        rename[loc_tag] = tag

    # Rename all references in `cells`
    exist_cells = join["cells"] if join is not None else {}
    elemgen = filter(lambda i: i not in exist_cells, count(estart))
    for k,conn in cells.items():
        exist_cells[next(elemgen)] = tuple(rename[n] for n in conn)

    return nodes, exist_cells

def grid(ne, nn=(2,2)):
    """
               |           ne[0] = 2       |

               |             | nn[0] = 3   |

          ---- +------+------+------+------+ ----
               |             |             |
               |             |             |
               |             |             | nn[1] = 2
               |             |             |
               |             |             |
               +------+------+------+------+ ----
               |             |             |
  ne[1] = 3    |             |             |
               |             |             |---------> s
               |             |             |
               |             |             |
               +------+------+------+------+
               |             |             |
               |             |             |
               |             |             |
               |             |             |
               |             |             |
          ---- +------+------+------+------+

    """
    nnx,nny = nn
    nex,ney = ne

    nx = nnx - 1
    ny = nny - 1

    cells = {
        k: [*(   (1+l) + i*nx + (j*ny+    0)*(nex*nx+1) for l in range(nnx)),
            *(    nnx  + i*nx + (j*ny+    l)*(nex*nx+1) for l in range(1,nny-1)),
            *(   (1+l) + i*nx + (j*ny+nny-1)*(nex*nx+1) for l in reversed(range(nnx))),
            *( -nex*nx + i*nx + (j*ny+nny-l)*(nex*nx+1) for l in range(1,nny-1))]

        for k,(j,i) in enumerate(product(range(ney), range(nex)))
    }

    used = {i for cell in cells.values() for i in cell}

    x, y = map(lambda n: np.linspace(-1, 1, n[0]*(n[1]-1)+1), ((nex,nnx),(ney,nny)))

    nodes = {
        i+1: (xi, yi) for i,(yi,xi) in enumerate(product(y,x)) if i+1 in used
    }

    return nodes, cells

def plot(nodes, cells):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    for cell in cells.values():
        ax.plot(*zip(*[nodes[i] for i in cell], nodes[cell[0]]))
    return ax

if __name__ == "__main__":
    import sys,pprint

    ne = int(sys.argv[1]), int(sys.argv[2])
    if len(sys.argv) > 3:
        nn = int(sys.argv[3]), int(sys.argv[4])

    else:
        nn = 2,2


    block_family = plane.Lagrange(4)
    points = {
            1: (0.0, 0.0),
            2: (1.0, 0.0),
            3: (1.0, 1.0),
            4: (0.0, 1.0),
            5: (0.5,-0.1)
    }

#   nodes, cells = grid(ne, nn)
#   nodes, cells = block(ne, plane.Lagrange(3))
    nodes, cells = block(ne, block_family, points=points)

    block_family = plane.Serendipity(4)
    points = {
            1: (1.0, 0.0),
            2: (2.0, 0.0),
            3: (2.0, 1.0),
            4: (1.0, 1.0),
            5: (1.5,-0.1)
    }
    nodes, cells = block(ne, block_family, points=points, join=dict(nodes=nodes, cells=cells))

#   pprint.PrettyPrinter(indent=4).pprint(nodes)
#   pprint.PrettyPrinter(indent=4).pprint(cells)

    from plotting import Plotter
    ax = plot(nodes, cells)
    ax.axis("equal")
#   ax = None
    Plotter(ax=ax).nodes(nodes).show()

