import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.chosen_target = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fill_dd_providers(self):
        for p in self.model.providers:
            self.view.dd_provider.options.append(ft.dropdown.Option(p))

    def handle_crea_grafo(self, e):
        if self.view.dd_provider.value is None or self.view.txt_distanza is None:
            self.view.create_alert("Selezionare un provider e inserire una distanza")
            return
        provider = self.view.dd_provider.value
        try:
            distanza = float(self.view.txt_distanza.value)
        except ValueError:
            self.view.create_alert("La distanza deve essere un numero in km")
            return
        graph = self.model.build_graph(provider, distanza)
        self.fill_dd_target(graph)
        self.view.btn_analisi.disabled = False
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {len(graph.nodes)} nodi e "
                                                     f"{len(graph.edges)} archi"))
        self.view.update_page()

    def fill_dd_target(self, graph):
        for node in graph.nodes:
            self.view.dd_target.options.append(ft.dropdown.Option(data=node,
                                                                  text=node,
                                                                  on_click=self.choose_target))

    def choose_target(self, e):
        if e.control.data is None:
            self.chosen_target = None
        self.chosen_target = e.control.data

    def handle_analisi(self, e):
        max_vicini = self.model.get_max_vicini()
        self.view.txt_stringa.disabled = False
        self.view.btn_percorso.disabled = False
        self.view.dd_target.disabled = False
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"I nodi con il numero massimo di vicini sono:"))
        for n in max_vicini:
            self.view.txt_result.controls.append(ft.Text(f"{n[0]}, {n[1]} vicini"))
        self.view.update_page()

    def handle_percorso(self, e):
        if self.chosen_target is None or self.view.txt_stringa.value is None:
            self.view.create_alert("Selezionare un target e inserire una stringa")
            return
        string = self.view.txt_stringa.value
        if string == "":
            self.view.create_alert("La stringa non può essere vuota")
            return
        path = self.model.get_percorso(self.chosen_target, string)
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Il percorso trovato ha lunghezza {len(path)}"))
        for p in path:
            self.view.txt_result.controls.append(ft.Text(p))
        self.view.update_page()

    @property
    def view(self):
        return self._view

    @property
    def model(self):
        return self._model
