def print_matrix(vertices, matrix):
  """
  Wypisuje na ekreanie graf zadany jako macierz sąsiedztwa
  """
  n = len(matrix)
  if (vertices is not None) and (len(vertices) == n):
    vv = vertices
  else:
    vv = range(1, n+1)
  for i in range(n):
    print(vv[i], ":", end="")
    for j in range(n):
      if matrix[i,j]:
        print(" ", vv[j], end="")
    print("")


def print_graph(graph):
  """
  Wypisuje graf zadany jako słownik pythona
  """
  for v in graph:
    print(v, ":", end="")
    for u in graph[v]:
      print(" ", u, end="")
    print("")
    

def add_vertex(graph, vertex):
    """Nowy wierzchołek do istniejącego grafu"""
    if vertex not in graph:
        graph[vertex] = []


def add_arc(graph, arc):
    """Dodaje nowy łuk (parę wierzchołków) do istniejącego grafu
       rozważamy grafy proste, skierowane
    """
    u, v = arc
    add_vertex(graph, u)
    add_vertex(graph, v)
    if v not in graph[u]:
        graph[u].append(v)


def add_edge(graph, edge):
    """Dodaje nową krawędź (parę wierzchołków) do istniejącego grafu
       traktując graf nieskierowany prosty jako prosty graf skierowany, ale symetryczny i bez pętli
    """
    u, v = edge
    add_vertex(graph, u)
    add_vertex(graph, v)
    if u == v:
        raise ValueError("pętla!")
    if v not in graph[u]:
        graph[u].append(v)
    if u not in graph[v]:
        graph[v].append(u)


def random_graph(n, p):
    """Tworzy graf losowy w modelu G(n, p) - graf nieskierowany, n wierzchołków, każda para połączona krawędzią
    niezależnie, z prawdopodobieństwem p"""
    random_graph = {}
    for i in range(1,n+1):
        add_vertex(random_graph, i)
    for i in range(1, n):
        for j in range(i+1,n+1):
            if random() <= p:
                add_edge(random_graph, (i,j))
    return random_graph


def graph_to_matrix(graph):
    """
     Konwertuje graf - listę sąsiedztwa na macierz (n^2)
    """
    vertices = list(graph.keys())
    index = {}
    i = 0
    for v in graph:
        index[v] = i
        i += 1
    matrix = np.zeros((len(vertices), len(vertices)))
    for v in graph:
        for u in graph[v]:
            matrix[index[v], index[u]] = 1
    return [vertices, matrix]


def matrix_to_graph(vertices, matrix):
  """
  Funkcja przekształcająca macierz sąsiedztwa na graf w formie listy sąsiedztwa
  """
  n = len(matrix)
  if (vertices is not None) and (len(vertices) == n):
    vv = vertices
  else:
    vv = range(1, n+1)
  graph = {}
  for i in range(n):
    edges = []
    for j in range(n):
      if matrix[i][j]:
        edges.append(vv[j])
    graph[vv[i]] = edges
  return graph


def ConnectedComponents(graph):
  """
  Znajduje spójne składowe w grafie nieskierowanym
  Jako wynik zwraca listę zbiorów wierzchołków
  Uwaga: pierwszym elementem zwracanej listy jest zbiór wszystkich wierzchołków grafu
  """
  def DFS(v):
    """
    Przeszukiwanie grafu w głąb
    """
    for u in graph[v]:
      if not u in VT[0]:    # u - jeszcze nie odwiedzony
        VT[0].add(u)        # u - już odwiedzony
        VT[-1].add(u)       # u - w ostatniej spójnej składowej
        DFS(u)

  """
  VT - lista zbiorów VT[i] dla i > 0 zbiór elementów i-tej spójnej składowej
  VT[0] = union_{i > 0} VT[i] - docelowo - zbiór wszystkich wierzchołków grafu
  """
  VT = [set([])]  
  for v in graph:
    if not v in VT[0]:
      VT[0].add(v)
      VT.append(set([v])) # zaczątek nowej, spójnej składowej
      DFS(v)
  return VT


def ConnectedComponentsGraphs(graph):
  """
  Zwraca spójne składowe grafu w formie listy grafów
  """
  VT = ConnectedComponents(graph)

  # Każdą spójną składową przepisujemy jako graf
  components = []
  for vt in VT[1:]:
    comp = {}
    for v in vt:
      comp[v] = graph[v].copy()
    components.append(comp)
  return components


def BFS(graph):
  v = list(graph.keys())[0]
  kolejnosc = []
  kolejka = []
  kolejka.append(v)
  while len(kolejka) > 0:
    u = kolejka.pop(0)
    kolejnosc.append(u)
    for w in graph[u]:
      if not w in kolejka and w not in kolejnosc:
        kolejka.append(w)
  return kolejnosc


def do_kolorowalnego_grafu(graph):
  graf_kolorowalny = {}
  for v in graph:
    graf_kolorowalny[v] = [graph[v], 'color']
  return graf_kolorowalny


def check_if_bipartite(graph):
  bipartite = True
  components = ConnectedComponentsGraphs(graph)
  for graph1 in components:		# przechodze po spojnych skladowych
    graph2 = do_kolorowalnego_grafu(graph1)	# przygotowuje graf do kolorowania (tworze wartosc na kolor)
    kolejnosc = BFS(graph1)			# kolejnosc kolorowania spojnej skladowej
    poprzednicy = []
    for v in kolejnosc:
      colors = [1, 2]				# lista kolorow do pokolorowania wierzcholka v
      dostepne = colors
      for u in poprzednicy:			# po poprzednikach wierzcholka v
        if u in graph1[v]:			# oraz sasiadach wierzcholka v
          color = graph2[u][1]
          if color in dostepne:
            dostepne.remove(color)		# usuwam kolor, ktorym zostal wczesniej pokolorowany sasiad wierzcholka v
      poprzednicy.append(v)
      if len(dostepne) == 0:			# jezeli nie ma dostepnych kolorow, to znaczy ze nie moge pokolorowac grafu 2 kolorami
        bipartite = False			# czyli graf nie jest dwudzielny
      else:
        graph2[v][1] = dostepne[0]		# w przeciwnym przypadku koloruje wierzcholek na pierwszy wolny kolor
      if not bipartite:
        break
    if not bipartite:
      break					# przerywam funkcje, gdy graf nie jest dwudzielny (wiecej mnie nie interesuje)
  if bipartite:					# informacja koncowa gdy graf jest lub nie jest dwudzielny
    print("Graf jest dwudzielny")
  else:
    print("Graf nie jest dwudzielny")