import random
from datetime import datetime, timedelta

class Ingredient(object): 
    _type = "" 
    _ultDate = ""

    def SerializerIngredient(self):
        result = None
        
        dato = []
        dato = {  "_type" : self._type,
               "_ultDate" : self._ultDate.strftime('%m/%d/%Y') }
        
        result = dato
        return result
    
    def randomIngredient():
        result = None

        ingrediente = Ingredient()
        ingrediente._type = random.choice(["MATCH", "PAPER", "TOBACCO"])
        ingrediente._ultDate = datetime.today() 

        result = ingrediente
        return result

    def factoryIngredient(tipo):
        result = None

        ingrediente = Ingredient()
        ingrediente._type = tipo
        ingrediente._ultDate = datetime.today() 

        result = ingrediente
        return result


class Bench(object): 
    _stock = []
    _flag = 0

    #Carga de la App
    def iniBench(NUM_INGREDIENTS_INIT,material):
        result = None
        stock = []
        for i in range(0,NUM_INGREDIENTS_INIT,1):
            stock.append( Ingredient.factoryIngredient(material) )
        
        result = stock
        return result


