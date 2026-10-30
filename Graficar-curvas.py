import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Graficos3D:

    def __init__(self, root):
        self.root = root
        self.root.title("Laboratorio Matemático 3D")
        self.root.geometry("1250x800")
        self.root.minsize(1000, 650)
        self.root.configure(bg="#101827")

        self.color_panel = "#1e293b"
        self.color_texto = "#f1f5f9"
        self.color_acento = "#38bdf8"

        self.variables = {}
        self.temporizador = None

        self.crear_interfaz()
        self.programar_actualizacion()

    def crear_interfaz(self):
        encabezado = tk.Frame(self.root, bg="#0f172a", height=85)
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        tk.Label(
            encabezado,
            text="LABORATORIO MATEMÁTICO 3D",
            font=("Segoe UI", 22, "bold"),
            fg="#38bdf8",
            bg="#0f172a"
        ).pack(pady=(13, 0))

        tk.Label(
            encabezado,
            text="Explora curvas y superficies en tiempo real",
            font=("Segoe UI", 10),
            fg="#cbd5e1",
            bg="#0f172a"
        ).pack()

        principal = tk.Frame(self.root, bg="#101827")
        principal.pack(fill="both", expand=True, padx=12, pady=12)

        panel = tk.Frame(
            principal,
            bg=self.color_panel,
            width=300
        )
        panel.pack(side="left", fill="y", padx=(0, 12))
        panel.pack_propagate(False)

        tk.Label(
            panel,
            text="CONFIGURACIÓN",
            font=("Segoe UI", 13, "bold"),
            fg=self.color_acento,
            bg=self.color_panel
        ).pack(pady=(15, 10))

        self.agregar_etiqueta(panel, "Tipo de gráfico")

        self.tipo = tk.StringVar(value="Esfera")

        opciones = [
            "Circunferencia 3D",
            "Elipse 3D",
            "Esfera",
            "Elipsoide",
            "Toroide",
            "Cilindro",
            "Cono",
            "Paraboloide",
            "Silla de montar",
            "Hélice"
        ]

        selector = ttk.Combobox(
            panel,
            textvariable=self.tipo,
            values=opciones,
            state="readonly"
        )
        selector.pack(fill="x", padx=15, pady=(0, 8))
        selector.bind(
            "<<ComboboxSelected>>",
            self.programar_actualizacion
        )

        self.agregar_etiqueta(panel, "Parámetros matemáticos")

        configuraciones = [
            ("Radio / escala X", "a", "2.0"),
            ("Escala Y", "b", "1.5"),
            ("Escala Z / altura", "c", "2.0"),
            ("Grosor del toroide", "r", "0.6"),
            ("Vueltas de hélice", "vueltas", "3.0"),
            ("Resolución (20-200)", "resolucion", "70")
        ]

        for etiqueta, clave, valor in configuraciones:
            fila = tk.Frame(panel, bg=self.color_panel)
            fila.pack(fill="x", padx=15, pady=3)

            tk.Label(
                fila,
                text=etiqueta,
                fg=self.color_texto,
                bg=self.color_panel,
                anchor="w"
            ).pack(fill="x")

            variable = tk.StringVar(value=valor)
            self.variables[clave] = variable

            tk.Entry(
                fila,
                textvariable=variable,
                bg="#0f172a",
                fg="white",
                insertbackground="white",
                relief="flat",
                font=("Consolas", 11)
            ).pack(fill="x", ipady=4, pady=(2, 0))

            variable.trace_add(
                "write",
                self.programar_actualizacion
            )

        self.agregar_etiqueta(panel, "Color de curvas")

        self.color = tk.StringVar(value="cyan")

        selector_color = ttk.Combobox(
            panel,
            textvariable=self.color,
            values=[
                "cyan",
                "deepskyblue",
                "royalblue",
                "magenta",
                "red",
                "orange",
                "lime",
                "gold",
                "black",
                "white"
            ],
            state="readonly"
        )
        selector_color.pack(fill="x", padx=15, pady=(0, 6))
        selector_color.bind(
            "<<ComboboxSelected>>",
            self.programar_actualizacion
        )

        self.agregar_etiqueta(panel, "Paleta de superficies")

        self.paleta = tk.StringVar(value="viridis")

        selector_paleta = ttk.Combobox(
            panel,
            textvariable=self.paleta,
            values=[
                "viridis",
                "plasma",
                "inferno",
                "magma",
                "cool",
                "winter",
                "spring",
                "turbo",
                "cividis"
            ],
            state="readonly"
        )
        selector_paleta.pack(fill="x", padx=15, pady=(0, 6))
        selector_paleta.bind(
            "<<ComboboxSelected>>",
            self.programar_actualizacion
        )

        self.agregar_etiqueta(panel, "Opacidad")

        self.opacidad = tk.DoubleVar(value=0.85)

        tk.Scale(
            panel,
            from_=0.1,
            to=1.0,
            resolution=0.05,
            orient="horizontal",
            variable=self.opacidad,
            bg=self.color_panel,
            fg="white",
            troughcolor="#334155",
            highlightthickness=0,
            command=lambda _: self.programar_actualizacion()
        ).pack(fill="x", padx=15)

        tk.Button(
            panel,
            text="ACEPTAR / APLICAR CAMBIOS",
            command=self.aplicar_cambios,
            bg="#0284c7",
            fg="white",
            activebackground="#0369a1",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        ).pack(fill="x", padx=15, pady=(12, 7), ipady=8)

        tk.Button(
            panel,
            text="Restablecer parámetros",
            command=self.restablecer,
            bg="#334155",
            fg="white",
            activebackground="#475569",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        ).pack(fill="x", padx=15, pady=(0, 10), ipady=6)

        self.estado = tk.StringVar(value="Preparando gráfico...")

        tk.Label(
            panel,
            textvariable=self.estado,
            fg="#7dd3fc",
            bg=self.color_panel,
            wraplength=265,
            justify="left"
        ).pack(fill="x", padx=15, pady=(0, 10))

        area_grafico = tk.Frame(principal, bg="white")
        area_grafico.pack(side="right", fill="both", expand=True)

        self.figura = Figure(figsize=(8, 6), dpi=100)
        self.figura.patch.set_facecolor("white")

        self.ax = self.figura.add_subplot(
            111,
            projection="3d"
        )

        self.canvas = FigureCanvasTkAgg(
            self.figura,
            master=area_grafico
        )
        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    def agregar_etiqueta(self, padre, texto):
        tk.Label(
            padre,
            text=texto,
            fg="#94a3b8",
            bg=self.color_panel,
            anchor="w",
            font=("Segoe UI", 9, "bold")
        ).pack(fill="x", padx=15, pady=(7, 3))

    def programar_actualizacion(self, *args):
        """Actualiza el gráfico tras una pausa de 450 milisegundos."""

        if self.temporizador is not None:
            try:
                self.root.after_cancel(self.temporizador)
            except tk.TclError:
                pass

        self.temporizador = self.root.after(
            450,
            self.actualizar_grafico
        )

    def aplicar_cambios(self):
        """Aplica los cambios inmediatamente."""

        if self.temporizador is not None:
            try:
                self.root.after_cancel(self.temporizador)
            except tk.TclError:
                pass

            self.temporizador = None

        self.actualizar_grafico()

    def obtener_numero(self, clave):
        texto = self.variables[clave].get().strip()
        texto = texto.replace(",", ".")

        if not texto:
            raise ValueError(
                f"El campo '{clave}' está vacío."
            )

        return float(texto)

    def restablecer(self):
        valores = {
            "a": "2.0",
            "b": "1.5",
            "c": "2.0",
            "r": "0.6",
            "vueltas": "3.0",
            "resolucion": "70"
        }

        for clave, valor in valores.items():
            self.variables[clave].set(valor)

        self.tipo.set("Esfera")
        self.color.set("cyan")
        self.paleta.set("viridis")
        self.opacidad.set(0.85)

        self.aplicar_cambios()

    def actualizar_grafico(self):
        self.temporizador = None

        try:
            a = self.obtener_numero("a")
            b = self.obtener_numero("b")
            c = self.obtener_numero("c")
            r = self.obtener_numero("r")
            vueltas = self.obtener_numero("vueltas")
            resolucion_valor = self.obtener_numero("resolucion")

            if not resolucion_valor.is_integer():
                raise ValueError(
                    "La resolución debe ser un número entero."
                )

            n = int(resolucion_valor)

            if min(a, b, c, r) <= 0:
                raise ValueError(
                    "Los radios y las escalas deben ser mayores que cero."
                )

            if vueltas <= 0:
                raise ValueError(
                    "Las vueltas deben ser mayores que cero."
                )

            if not 20 <= n <= 200:
                raise ValueError(
                    "La resolución debe estar entre 20 y 200."
                )

            self.dibujar(a, b, c, r, vueltas, n)

            self.estado.set(
                f"Gráfico actualizado: {self.tipo.get()}"
            )

        except (ValueError, TypeError) as error:
            self.estado.set(
                f"Revisa los parámetros: {error}"
            )

        except Exception as error:
            self.estado.set(
                f"Error al dibujar: {error}"
            )

    def dibujar(self, a, b, c, r, vueltas, n):
        self.ax.clear()

        color = self.color.get()
        paleta = self.paleta.get()
        alpha = float(self.opacidad.get())
        tipo = self.tipo.get()

        u = np.linspace(0, 2 * np.pi, n)
        v = np.linspace(0, np.pi, n)
        U, V = np.meshgrid(u, v)

        if tipo == "Circunferencia 3D":
            t = np.linspace(0, 2 * np.pi, n * 2)

            x = a * np.cos(t)
            y = a * np.sin(t)
            z = c * 0.4 * np.sin(2 * t)

            self.ax.plot(
                x, y, z,
                color=color,
                linewidth=3
            )

        elif tipo == "Elipse 3D":
            t = np.linspace(0, 2 * np.pi, n * 2)

            x = a * np.cos(t)
            y = b * np.sin(t)
            z = c * 0.5 * np.sin(t)

            self.ax.plot(
                x, y, z,
                color=color,
                linewidth=3
            )

        elif tipo == "Esfera":
            x = a * np.cos(U) * np.sin(V)
            y = a * np.sin(U) * np.sin(V)
            z = a * np.cos(V)

            self.ax.plot_surface(
                x, y, z,
                cmap=paleta,
                alpha=alpha,
                linewidth=0,
                antialiased=True
            )

        elif tipo == "Elipsoide":
            x = a * np.cos(U) * np.sin(V)
            y = b * np.sin(U) * np.sin(V)
            z = c * np.cos(V)

            self.ax.plot_surface(
                x, y, z,
                cmap=paleta,
                alpha=alpha,
                linewidth=0,
                antialiased=True
            )

        elif tipo == "Toroide":
            x = (a + r * np.cos(V)) * np.cos(U)
            y = (a + r * np.cos(V)) * np.sin(U)
            z = r * np.sin(V)

            self.ax.plot_surface(
                x, y, z,
                cmap=paleta,
                alpha=alpha,
                linewidth=0
            )

        elif tipo == "Cilindro":
            theta = np.linspace(0, 2 * np.pi, n)
            altura = np.linspace(-c, c, n)
            T, Z = np.meshgrid(theta, altura)

            X = a * np.cos(T)
            Y = a * np.sin(T)

            self.ax.plot_surface(
                X, Y, Z,
                cmap=paleta,
                alpha=alpha,
                linewidth=0
            )

        elif tipo == "Cono":
            theta = np.linspace(0, 2 * np.pi, n)
            altura = np.linspace(0, c, n)
            T, Z = np.meshgrid(theta, altura)

            radio = a * (1 - Z / c)
            X = radio * np.cos(T)
            Y = radio * np.sin(T)

            self.ax.plot_surface(
                X, Y, Z,
                cmap=paleta,
                alpha=alpha,
                linewidth=0
            )

        elif tipo == "Paraboloide":
            x = np.linspace(-a, a, n)
            y = np.linspace(-b, b, n)
            X, Y = np.meshgrid(x, y)

            Z = c * (
                (X / a) ** 2 +
                (Y / b) ** 2
            )

            self.ax.plot_surface(
                X, Y, Z,
                cmap=paleta,
                alpha=alpha,
                linewidth=0
            )

        elif tipo == "Silla de montar":
            x = np.linspace(-a, a, n)
            y = np.linspace(-b, b, n)
            X, Y = np.meshgrid(x, y)

            Z = c * (
                (X / a) ** 2 -
                (Y / b) ** 2
            )

            self.ax.plot_surface(
                X, Y, Z,
                cmap=paleta,
                alpha=alpha,
                linewidth=0
            )

        elif tipo == "Hélice":
            t = np.linspace(
                0,
                2 * np.pi * vueltas,
                n * 10
            )

            x = a * np.cos(t)
            y = b * np.sin(t)
            z = c * t / (2 * np.pi)

            self.ax.plot(
                x, y, z,
                color=color,
                linewidth=3
            )

        self.ax.set_title(
            tipo,
            fontsize=16,
            fontweight="bold",
            pad=18
        )

        self.ax.set_xlabel("Eje X", labelpad=8)
        self.ax.set_ylabel("Eje Y", labelpad=8)
        self.ax.set_zlabel("Eje Z", labelpad=8)

        self.ax.set_facecolor("#f8fafc")
        self.ax.grid(True, alpha=0.25)
        self.ax.view_init(elev=25, azim=40)

        self.figura.tight_layout()
        self.canvas.draw_idle()


if __name__ == "__main__":
    ventana = tk.Tk()
    aplicacion = Graficos3D(ventana)
    ventana.mainloop()