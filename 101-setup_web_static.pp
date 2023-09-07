# pupet manfest config nginx
exec { 'run1':
  command => 'sudo apt-get -y update',
  path    => [ '/usr/local/bin/', '/usr/bin/', '/bin/' ]
}
exec { 'run2':
  command => 'sudo apt-get -y install nginx',
  path    => [ '/usr/local/bin/', '/usr/bin/', '/bin/' ]
}
exec { 'run3':
  command => 'sudo mkdir -p /data/web_static/shared/',
  path    => [ '/usr/local/bin/', '/usr/bin/', '/bin/' ]
}
exec { 'run4':
  command => 'sudo mkdir -p /data/web_static/releases/test/',
  path    => [ '/usr/local/bin/', '/usr/bin/', '/bin/' ]
}
file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => 'this is simple content'
}
exec { 'run4':
  command => 'sudo ln -sf /data/web_static/releases/test/ /data/web_static/current',
  path    => [ '/usr/local/bin/', '/usr/bin/', '/bin/' ]
}
exec { 'change_permission':
  command => 'sudo chown -R ubuntu:ubuntu /data/',
  path    => [ '/usr/local/bin/', '/usr/bin/', '/bin/' ]
}
file_line { 'add_location':
  ensure => 'present',
  path   => '/etc/nginx/sites-available/default',
  after  => 'server_name _;',
  line   => '\\\tlocation /hbnb_static {\n\\\t\\\talias /data/web_static/current/;\n\\\t}'
}
exec { 'restart':
  command => 'sudo service nginx restart',
  path    => [ '/usr/bin/', '/bin/' ]
}
