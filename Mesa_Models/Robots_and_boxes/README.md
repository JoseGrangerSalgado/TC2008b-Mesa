# Team

-  Jose Granger - A01023661
-  Jorge Cabiedes - A01024053

## Diagrama de Clase y Protocolo de Agentes

![](https://i.imgur.com/RQJtrDx.png)

## Jerarquia de Acciones

* Checar si agente esta cargando caja
    * Agente tiene caja (MoveFull) : 
        * Correr algoritmo de pathfinding (cajas son obstaculos)
        * Mover agente segun coordenadas
        * Mover caja segun coordenadas
    * Agente no tiene caja (moveEmpty) : 
        * Mover agente en una direccion random sin obstaculos (cajas no son obstaculos)
* Checar si se encuentra una caja en la posición, en caso de encontrarse, modificar Robot a que tenga caja
* Checar si el agente se encuentra en el objetivo, en caso de encontrarse, modificar Agente a que no tenga caja y borrar caja.

## Funcionamiento

Los agentes(robots) se mueven de una forma aleatoria en el grid hasta que encuentran una caja, despues de lo cual cambia el estado interno del robot a que esta cargando una caja y se corre la funcion de MoveFull en vez de moveEmpty.

En esta funcion se usa una matriz que creamos al inicio del programa del tamaño del grid donde asignamos a los lugares vacios un valor de 1, a los lugares con obstaculos un valor de casi infinito y el destino un valor de 2. Usamos un pathfinding algorithm para encontrar el camino mas eficiente desde el lugar del agente al destino y regresamos el array de coordenadas para que lo sigan al moverse el robot y la caja.

Una vez entregada la caja en el destino se borra este agente(caja) y el robot regresa a su estado inicial de vacio.

Mientras tanto, en el background se corre un server de Flask que contiene varios endpoints con los cuales interactua Unity.

El endpoint de /init, cual se usas para iniciar el modelo de Mesa y definir todas las variables necesarias para crear el modelo en si.

El endpoint de /getRobots consigue las coordenadas de los robots y las manda sorteadas para que Unity sepa que coordenadas asignar a que agente.

El endpoint de /getBoxes realiza lo mismo que endpoint de Robots pero para las cajas.

El endpoint de /getObj realiza los mismo pero para el objetivo, las coordenadas del objetivo al ser las mismas no se necesitan actualizar.

Finalmente, el endpoint de /update es el que ordena a Mesa a continuar al siguiente paso.

En Unity, creamos prefabs de todos los objetos necesarios y usamos lo aprendido en clase para darle un smooth movement a estos objetos.

Primero inicializamos todas las variables que vamos a usar, tanto como de los agentes,endpoints,posiciones y configuraciones.

Despues de esto creamos todos los agentes y objetos necesarios y corremos las rutinas para empezar la simulacion de Mesa y conseguir las posiciones de todo lo necesario, asignando los agentes y objetos a las posiciones recuperadas por nuestro endpoint.

Al final, usando la función de Update() en Unity usando la variable de timer definimos que tan rapido se muevan los agentes y nos aseguramos de actualizar la simulación, recuperando las posiciones de los agentes y despues de las cajas para mantener la logica y usando el metodo de smooth movement aprendido en clase.

## Pruebas



| # de Prueba | Num. Robots | % de cajas | # de pasos a terminar |
| ----------- | ----------- | ---------- | ------------------- |
| Prueba 1    | 2           | 67         |   312                  |
| Prueba 2    |   6          |    40        |     131               |
| Prueba 3    |    3         |    20        |   97                  |
| Prueba 4    | 8       | 80      |   183                      |     |

## Reflexion

Logramos llegar a una eficiencia buena gracias a nuestro pathfinding algorithm, los robots casi siempre regresan de la forma mas eficiente al origen lo cual reduce mucho el tiempo que toma. Aun asi un aspecto muy ineficiente es que busca las cajas de una forma aleatoria, una mejora en este aspecto puede ser que las cajas se comuniquen entre si las locaciones de las cajas que encuentren para que no tengan que buscarlas todas al mismo tiempo.

Otro problema que vimos es que asumimos desde el inicio que los robots saben el layout de todo el grid cuando esa no es probablemente la situacion, un cambio seria ir adaptando la forma de encontrar el destino segun las posiciones descubiertas por los robots.

Fuera de esto, probablemente podemos optimizar nuestro algorithmo de pathfinding para que no tenga que correrse tantas veces, seria que un solo robot scout haga el analisis y se los mande a los demas robots o una forma que ocupe menos tiempo y espacio como usando reglas geometricas.

Un problema que encontramos con el sistema actual es que si hay muchos elementos(robots) es un poco lento y si esta tapado el origen y no se pueden mover estan atrapados permanentemente.

Otra mejora podria ser que los dispositivos se comuniquen entre si sus locaciones para que puedan evitar obstruirse mutuamente.

Finalmente un problema es que presentamente el programa corre por mucho tiempo y no se le puede poner un limite de tiempo o alguna forma de hacer un tracking de progreso a lo largo de una determinación de tiempo, algo que tendria que mejorarse para el futuro.
