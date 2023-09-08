from fabric.api import env, put, run
from os.path import exists

# Configure the web server IPs
env.hosts = ['34.229.56.92', '54.236.27.183>']
# Set the SSH username
env.user = 'ubuntu'
# Set the path to the web server directory
env.deploy_path = '/data/web_static'


def do_deploy(archive_path):
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the web server
        put(archive_path, '/tmp/')
        
        # Extract the archive to a new release folder
        archive_filename = archive_path.split('/')[-1]
        release_folder = '/'.join(archive_filename.split('.')[:-1])
        release_path = '{}/releases/{}'.format(env.deploy_path, release_folder)
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_path))
        
        # Remove the uploaded archive
        run('rm /tmp/{}'.format(archive_filename))
        
        # Remove the current symbolic link
        run('rm -f {}/current'.format(env.deploy_path))
        
        # Create a new symbolic link to the new release
        run('ln -s {} {}/current'.format(release_path, env.deploy_path))
        
        return True
    except:
        return False
