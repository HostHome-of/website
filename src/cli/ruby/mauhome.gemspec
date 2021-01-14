Gem::Specification.new do |s|
    s.name      = 'mauhome'
    s.version   = '1.0.0'
    s.platform  = Gem::Platform::RUBY
    s.summary   = 'El CLI para HostHome'
    s.description = "Creado para poder hacer host en HostHome"
    s.authors   = ['Maubg']
    s.homepage  = 'http://github.com/maubg-debug/host'
    s.license   = 'MIT'
    s.files     = Dir.glob("{lib,bin}/**/*")
    s.require_path = 'lib'
end