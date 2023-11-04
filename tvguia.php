<?php
error_reporting(0);
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

// Crear arreglos de opciones para los filtros
$categorias = array_unique(array_column($tvPrograms, 'categoria'));
$tipos = array_unique(array_column($tvPrograms, 'tipo'));
$canales = array_unique(array_column($tvPrograms, 'canal'));
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Programas de TV</title>
</head>
<body>
    <h1>Programas de TV</h1>
    
    <!-- Formulario de filtros -->
    <form method="post">
        <label for="categoria">Categoría:</label>
        <select name="categoria" id="categoria">
            <option value="">Todos</option>
            <?php foreach ($categorias as $categoria) : ?>
                <option value="<?php echo $categoria; ?>"><?php echo $categoria; ?></option>
            <?php endforeach; ?>
        </select>

        <label for="tipo">Tipo:</label>
        <select name="tipo" id="tipo">
            <option value="">Todos</option>
            <?php foreach ($tipos as $tipo) : ?>
                <option value="<?php echo $tipo; ?>"><?php echo $tipo; ?></option>
            <?php endforeach; ?>
        </select>

        <label for="canal">Canal:</label>
        <select name="canal" id="canal">
            <option value="">Todos</option>
            <?php foreach ($canales as $canal) : ?>
                <option value="<?php echo $canal; ?>"><?php echo $canal; ?></option>
            <?php endforeach; ?>
        </select>

        <input type="submit" value="Filtrar">
    </form>

    <!-- Tabla de programas -->
    <table style="width: 100%;">
    <!-- Encabezados de la tabla -->
    <tr>
        <th style="width: 50px;">Canal</th>
        <th style="width: 3%;">Logo</th>
        <th style="width: 5%;">Fecha</th>
        <th style="width: 3%;">Hora</th>
        <th style="width: 5%;">Título</th>
        <th style="width: 50%;">Descripción</th>
        <th style="width: 5%;">Tipo</th>
        <th style="width: 5%;">Categoría</th>
        <th style="width: 10%;">Imagen</th>
    </tr>
    <?php
    error_reporting(0); // Desactivar la visualización de errores
    // Filtrar programas según los valores seleccionados en los combobox
    $categoriaFiltro = isset($_POST['categoria']) ? $_POST['categoria'] : '';
    $tipoFiltro = isset($_POST['tipo']) ? $_POST['tipo'] : '';
    $canalFiltro = isset($_POST['canal']) ? $_POST['canal'] : '';

    foreach ($tvPrograms as $program) {
        if (($categoriaFiltro == '' || $program->categoria == $categoriaFiltro) &&
            ($tipoFiltro == '' || $program->tipo == $tipoFiltro) &&
            ($canalFiltro == '' || $program->canal == $canalFiltro)) {
            echo '<tr>';
            echo '<td>' . $program->canal . '</td>';
            echo '<td><img src="' . $program->logo . '" alt="' . $program->canal . '"></td>';
            echo '<td>' . $program->fecha . '</td>';
            echo '<td>' . $program->hora . '</td>';
            echo '<td>' . $program->titulo . '</td>';
            echo '<td>' . $program->descripcion . '</td>';
            echo '<td>' . $program->tipo . '</td>';
            echo '<td>' . $program->categoria . '</td>';
            echo '<td><img src="' . $program->imagen . '" alt="Imagen de ' . $program->titulo . '"></td>';
            echo '</tr>';
        }
    }
    error_reporting(E_ALL); // Restaurar la visualización de errores
    ?>
</table>
</body>
</html>
