# Agenda_IAinteractive
Prueba realizada para IAinteractive
**Este Crud fue realizado con el framwork flask en python 3.9, instalar la versión 3.9 mediante pip para poder ejecutarlo. **
**Instalar flask desdde la terminal utilizando el comando pip install flask y pip install flask-mysqldb para la base de datos **
**Instalar jinji2 mediante el comando pip install jinja2 **
**para arrancar la app solo se debe posicionar en la carpeta raiz, donde esta el archivo app.py, e inicar el servidor con el comando python app.py *
**la carpeta ide no contiene archivos necesarios para la ejecución de la aplicación, fue creada por el ide de pycharm**

Los campos de telefono y correo solo tienene validadción para no duplicarse en la base de dator con la propiedad unique


scrip de base de datos:

CREATE DATABASE `contacts`

CREATE TABLE IF NOT EXISTS `contactos` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `apellido_paterno` varchar(255) NOT NULL,
  `apellido_materno` varchar(255) DEFAULT NULL,
  `telefono` varchar(255) NOT NULL,
  `correo` varchar(255) NOT NULL,
  `foto` varchar(5000) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `telefono` (`telefono`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `contactos`
--

INSERT INTO `contactos` (`id`, `nombre`, `apellido_paterno`, `apellido_materno`, `telefono`, `correo`, `foto`) VALUES
(25, 'Jaime', 'Manguem', 'Yam', '9994851253', 'capitanmanguem@gmail.com', '2021020623ManguemYamJaime.jpg'),
(26, 'Gizem', 'Bayraktar', 'Manguem', '9994851275', 'gizembayraktar@gmail.com', '20210207011608900573183.jpg');
COMMIT;
