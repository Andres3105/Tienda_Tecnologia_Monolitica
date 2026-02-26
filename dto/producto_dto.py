class ProductoDTO:
    def __init__(self, id, nombre, descripcion, precio, stock, imagen=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.imagen = imagen