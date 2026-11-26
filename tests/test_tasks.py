import unittest
from tasks import agregar_tarea, completar_tarea, eliminar_tarea, pendientes


class TestTasks(unittest.TestCase):
    def test_agregar_tarea(self):
        tareas = []
        tarea = agregar_tarea(tareas, "Leer documentación")
        self.assertEqual(tarea["titulo"], "Leer documentación")
        self.assertFalse(tarea["completada"])

    def test_completar_tarea(self):
        tareas = []
        agregar_tarea(tareas, "Practicar")
        completar_tarea(tareas, 1)
        self.assertEqual(pendientes(tareas), [])

    def test_categoria_valida(self):
        tareas = []
        tarea = agregar_tarea(tareas, "Estudiar", "Universidad")
        self.assertEqual(tarea["categoria"], "Universidad")

    def test_categoria_por_defecto(self):
        tareas = []
        tarea = agregar_tarea(tareas, "Leer")
        self.assertEqual(tarea["categoria"], "general")

    def test_categoria_vacia(self):
        tareas = []
        with self.assertRaises(ValueError):
            agregar_tarea(tareas, "Leer", "")
        with self.assertRaises(ValueError):
            agregar_tarea(tareas, "Leer", "   ")
        self.assertEqual(tareas, [])

    def test_filtrado_por_categoria(self):
        tareas = []
        agregar_tarea(tareas, "A", "Casa")
        agregar_tarea(tareas, "B", "Trabajo")
        agregar_tarea(tareas, "C", "casa")
        completar_tarea(tareas, 3)
        resultado = pendientes(tareas, "CASA")
        self.assertEqual([t["titulo"] for t in resultado], ["A"])
        self.assertEqual(len(pendientes(tareas)), 2)
        self.assertEqual(pendientes(tareas, "otra"), [])

    def test_filtrar_categoria_inexistente_devuelve_lista_vacia(self):
        tareas = []
        agregar_tarea(tareas, "A", "Casa")
        self.assertEqual(pendientes(tareas, "inexistente"), [])

    def test_filtrar_categoria_vacia_lanza_error(self):
        tareas = []
        agregar_tarea(tareas, "A", "Casa")
        with self.assertRaises(ValueError):
            pendientes(tareas, "   ")
        with self.assertRaises(ValueError):
            pendientes(tareas, "")

    def test_eliminar_tarea_correcta(self):
        tareas = []
        agregar_tarea(tareas, "A")
        b = agregar_tarea(tareas, "B")
        eliminada = eliminar_tarea(tareas, 2)
        self.assertIs(eliminada, b)
        self.assertEqual([t["id"] for t in tareas], [1])

    def test_eliminar_tarea_inexistente(self):
        tareas = []
        agregar_tarea(tareas, "A")
        with self.assertRaises(ValueError) as ctx:
            eliminar_tarea(tareas, 99)
        self.assertEqual(str(ctx.exception), "Tarea no encontrada")
        self.assertEqual([t["id"] for t in tareas], [1])

    def test_id_unico_despues_de_eliminar(self):
        tareas = []
        agregar_tarea(tareas, "A")
        agregar_tarea(tareas, "B")
        agregar_tarea(tareas, "C")
        eliminar_tarea(tareas, 2)
        nueva = agregar_tarea(tareas, "D")
        ids = [t["id"] for t in tareas]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(nueva["id"], 4)


if __name__ == "__main__":
    unittest.main()
