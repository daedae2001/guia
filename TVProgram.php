<?php

// Clase para representar un programa de televisión
class TVProgram {
    public $canal;
    public $logo;
    public $fecha;
    public $hora;
    public $titulo;
    public $descripcion;
    public $tipo;
    public $categoria;
    public $imagen;

    public function __construct($canal, $logo, $fecha, $hora, $titulo, $descripcion, $tipo, $categoria, $imagen) {
        $this->canal = $canal;
        $this->logo = $logo;
        $this->fecha = $fecha;
        $this->hora = $hora;
        $this->titulo = $titulo;
        $this->descripcion = $descripcion;
        $this->tipo = $tipo;
        $this->categoria = $categoria;
        $this->imagen = $imagen;
    }
}

// Lista para almacenar objetos TVProgram
$tvPrograms = [];

// Ruta al archivo CSV
$csvFile = 'tv_program.csv';

// Lee los datos del archivo CSV
if (($handle = fopen($csvFile, "r")) !== FALSE) {
    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
        $program = new TVProgram(
            $data[0], // canal
            $data[1], // logo
            $data[2], // fecha
            $data[3], // hora
            $data[4], // titulo
            $data[5], // descripcion
            $data[6], // tipo
            $data[7], // categoria
            $data[8]  // imagen
        );
        $tvPrograms[] = $program;
    }
    fclose($handle);
}

// Ahora tienes una lista de objetos TVProgram que puedes usar en tu página web
?>
