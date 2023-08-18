import os
import subprocess  # nosec


def build_go_binary(goos, goarch, binary_name):
    os.environ['GOOS'] = goos
    os.environ['GOARCH'] = goarch
    subprocess.check_call(['go', 'build', '-o', # nosec
        os.path.join('.', 'apoplan', binary_name),
        os.path.join('.', 'cli-go')])

def main():
    # todo
    # platforms = ['darwin', 'linux', 'windows']
    # architectures = ['amd64', 'arm64']

    build_go_binary('darwin', 'arm64', 'bauplan-cli')

if __name__ == '__main__':
    main()
