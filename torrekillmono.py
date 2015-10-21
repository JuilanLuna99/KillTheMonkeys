#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pilasengine
import random

fin_de_juego = False

pilas = pilasengine.iniciar()

pilas.fondos.Pasto()
puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.naranja)
puntos.magnitud = 40
pilas.actores.Sonido()

# Variables y Constantes
balas_simples = pilas.actores.Bala
monos = []


# Funciones
def mono_destruido(disparo,enemigo):
    efecto = random.uniform(.25,.75)
    enemigo.eliminar()
    disparo.eliminar()
    puntos.aumentar()
    puntos.escala = (2,efecto),.5
    a=monos.index(enemigo)
    del monos[a]

def perder(torreta, enemigo):
    # Indicar fin de juego y eliminar lo que ya no se necesita
    global fin_de_juego
    enemigo.sonreir()
    torreta.eliminar()
    aviso=pilas.actores.Texto("GAME OVER")
    aviso.y = -100
    aviso.definir_color(pilas.colores.naranja)
    pilas.avisar("Conseguiste %d puntos" % (puntos.obtener()))
    fin_de_juego=True


def crear_mono():
    efecto = random.uniform(.25,.75)
    # Crear un enemigo nuevo
    enemigo = pilas.actores.Mono()
    # Hacer que se aparición sea con un efecto bonito
    ##la escala varíe entre 0,25 y 0,75 (Ojo con el radio de colisión)
    enemigo.escala = (1,efecto),.25
    enemigo.radio_de_colision = efecto*50
    # Dotarle de la habilidad de que explote al ser alcanzado por un disparo
    enemigo.aprender(pilas.habilidades.PuedeExplotar)
    # Situarlo en una posición al azar, no demasiado cerca del jugador
    x = random.randrange(-320, 320)
    y = random.randrange(-240, 240)
    if x >= 0 and x <= 100:
        x = 180
    elif x <= 0 and x >= -100:
        x = -180
    if y >= 0 and y <= 100:
        y = 180
    elif y <= 0 and y >= -100:
        y = -180
    enemigo.x = x
    enemigo.y = y
    # Dotarlo de un movimiento irregular más impredecible
    #tipo_interpolacion = ['lineal',
   #                         'aceleracion_gradual',
   #                         'desaceleracion_gradual',
   #                         'rebote_inicial',
   #                         'rebote_final']
    
    duracion = 1 +random.random()*4
    
    pilas.utils.interpolar(enemigo, 'x', 0, duracion)
    pilas.utils.interpolar(enemigo, 'y', 0, duracion)
    #enemigo.x = pilas.interpolar(0,tiempo,tipo=random.choice(tipo_interpolacion))
    #enemigo.y = pilas.interpolar(0, tiempo,tipo=random.choice(tipo_interpolacion))
    # Añadirlo a la lista de enemigos
    monos.append(enemigo)
    if random.randrange(0,20)>15:
        if torreta.municion!=pilasengine.actores.Misil:
            estrella = pilas.actores.Estrella(x,y)
            estrella.escala=[3,0,1],.1
            pilas.colisiones.agregar(estrella,torreta.habilidades.DispararConClick.proyectiles,asignar_arma_mejorada)
            pilas.tareas.agregar(3, eliminar_estrella, estrella)

    # Permitir la creación de enemigos mientras el juego esté en activo
    if fin_de_juego:
        return False
    else:
        return True

def asignar_arma_simple():
    # Asignar la munición sencilla
    torreta.municion=pilasengine.actores.Bala

def asignar_arma_mejorada(estrella, proyectil):
    global torreta
    torreta.municion=pilasengine.actores.Misil
    estrella.eliminar()
    pilas.tareas.agregar(10, asignar_arma_simple)
    pilas.avisar("MEJORA DE ARMA ACTIVADA")

def eliminar_estrella(estrella):
    estrella.eliminar()



# Añadir la torreta del jugador

torreta = pilas.actores.Torreta(enemigos=monos, cuando_elimina_enemigo=mono_destruido)

pilas.tareas.agregar(1, crear_mono)
#pilas.mundo.agregar_tarea(1, crear_mono) <-- sintaxis vieja

pilas.colisiones.agregar(torreta,monos,perder)

# Arrancar el juego
pilas.ejecutar()