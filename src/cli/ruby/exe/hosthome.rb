require 'optparse'
require "uri"

@verbose = false

@ayuda = File.open("./src/cli/ayuda.txt", "r").read
@texto = File.open("./src/cli/archivo.txt", "r").read

@main = ""
@ins = ""

OptionParser.new do |opts|
  opts.on("-h", "--help", "Enseña el comando de ayuda") do
    puts @ayuda
    exit
  end
  opts.on("-v", "--verbose", "te dice lo que esta creando") do
    @verbose = true
  end
  opts.on("empezar", "Empezar la instalacion") do

    while true # Archivo principal
      puts "Pon donde estara el archivo principal * :: (Tiene que terminar con .rb)"
      main = gets
      if main == ""
        next
      elsif !main.end_with?(".rb")
      end
      @main = main
      break
    end

    @texto.gsub! 'mainTemp', @main
    @texto.gsub! 'instalacionTemp', "bundle install"

    if @verbose == true
      puts "Creando archivo en ruta padre ..."
      File.open(".host.home", "w") { 
        |file| file.puts @texto
      }
      sleep(1)
      puts "Escribiendo ..."
      sleep(1)
      puts "Ya esta"
      exit
    else
      File.open(".host.home", "w") { 
        |file| file.puts @texto
      }
    end
  end
module hosthome
end