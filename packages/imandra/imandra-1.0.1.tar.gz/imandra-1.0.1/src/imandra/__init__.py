#!/usr/bin/python3
from . import ipl
from .auth import Auth
from . import instance
from . import rule_synth
from . import cfb
from . import core
from .session import HttpInstanceSession


def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser(prog="imandra", description="Imandra CLI")

    parser.set_defaults(run=lambda args: parser.print_help())
    subparsers = parser.add_subparsers()

    auth = Auth()

    parser_auth = subparsers.add_parser('auth')
    parser_auth.set_defaults(run=lambda args: parser_auth.print_help())
    parser_auth_subparsers = parser_auth.add_subparsers()

    def login(args):
        auth.login()
        print("Logged in")

    parser_login = parser_auth_subparsers.add_parser('login')
    parser_login.set_defaults(run=login)

    def logout(args):
        auth.logout()
        print("Logged out")

    parser_logout = parser_auth_subparsers.add_parser('logout')
    parser_logout.set_defaults(run=logout)

    parser_export = parser_auth_subparsers.add_parser('export')
    parser_export.set_defaults(run=lambda args: auth.export())

    parser_import = parser_auth_subparsers.add_parser('import')
    parser_import.set_defaults(run=lambda args: auth.import_())

    parser_ipl = subparsers.add_parser('ipl')
    parser_ipl.set_defaults(run=lambda args: parser_ipl.print_help())
    parser_ipl_subparsers = parser_ipl.add_subparsers()


    def ipl_decompose(args):
        if args.file is not None and args.parent_job_id is not None:
            print("error: --file and --parent-job-id are mutually exclusive operations. "
                  "You must pick one or the other")
            sys.exit(1)
        if args.file is None and args.parent_job_id is None:
            print ('error: --file must be provided')
        else:
            ipl.decompose(auth, args.file, args.testgen_lang, args.organization,
                                  args.callback, args.doc_gen, args.parent_job_id)


    parser_ipl_decompose = parser_ipl_subparsers.add_parser('decompose')


    parser_ipl_decompose.add_argument('--file')
    parser_ipl_decompose.add_argument('--callback')
    parser_ipl_decompose.add_argument('--testgen-lang', help=argparse.SUPPRESS)
    parser_ipl_decompose.add_argument('--organization')
    parser_ipl_decompose.add_argument('--doc-gen', choices=['true','false'], default='true')
    parser_ipl_decompose.add_argument('--parent-job-id',
                                      help=("The id of a previously completed job. Instead of running a "
                                            "full decomposition, re-run just the script generation phase of "
                                            "this parent-job. When using this option all other options will be "
                                            "ignore and the original values from the parent-job will be used."))
    parser_ipl_decompose.set_defaults(run=ipl_decompose)

    def ipl_simulator(args):
        if args.file is None:
            print ('error: --file must be provided')
        else:
            ipl.simulator(auth, args.file)

    parser_ipl_simulator = parser_ipl_subparsers.add_parser('simulator')
    parser_ipl_simulator.add_argument('--file')
    parser_ipl_simulator.set_defaults(run=ipl_simulator)

    def ipl_status(args):
        if args.uuid is None:
            print ('error: --uuid must be provided')
        else:
            ipl.status(auth, args.uuid)

    parser_ipl_status = parser_ipl_subparsers.add_parser('status')
    parser_ipl_status.add_argument('--uuid')
    parser_ipl_status.set_defaults(run=ipl_status)

    def ipl_data(args):
        if args.uuid is None:
            print ('error: --uuid must be provided')
        else:
            ipl.data(auth, args.uuid)

    parser_ipl_decompose = parser_ipl_subparsers.add_parser('data')
    parser_ipl_decompose.add_argument('--uuid')
    parser_ipl_decompose.set_defaults(run=ipl_data)

    parser_ipl_jobs = parser_ipl_subparsers.add_parser('list-jobs')
    parser_ipl_jobs.set_defaults(run=lambda args: ipl.list_jobs(auth))

    def ipl_cancel(args):
        if args.uuid is None:
            print ('error: --uuid must be provided')
        else:
            ipl.cancel(auth, args.uuid)

    parser_ipl_cancel = parser_ipl_subparsers.add_parser('cancel')
    parser_ipl_cancel.add_argument('--uuid')
    parser_ipl_cancel.set_defaults(run=ipl_cancel)

    parser_core = subparsers.add_parser('core')
    parser_core.set_defaults(run=lambda args: parser_core.print_help())
    parser_core_subparsers = parser_core.add_subparsers()

    parser_instances = parser_core_subparsers.add_parser('instances')
    parser_instances.set_defaults(run=lambda args: parser_instances.print_help())
    parser_instances_subparsers = parser_instances.add_subparsers()

    parser_instances_list = parser_instances_subparsers.add_parser('list')
    parser_instances_list.set_defaults(run=lambda args: instance.list(auth))

    def create_instance(args):
        if args.instance_type is None:
            print ('error: --instance-type must be provided')
        else:
            instance.create(auth, args.version, args.instance_type)

    parser_instances_create = parser_instances_subparsers.add_parser('create')
    parser_instances_create.add_argument('--instance-type')
    parser_instances_create.add_argument('--version')
    parser_instances_create.set_defaults(run=create_instance)

    def kill_instance(args):
        if args.id is None:
            print ('error: --id must be provided')
        else:
            instance.delete(auth, args.id)

    parser_instances_kill = parser_instances_subparsers.add_parser('kill')
    parser_instances_kill.add_argument('--id')
    parser_instances_kill.set_defaults(run=kill_instance)

    def rule_synth(args):
        if args.file is None:
            print ('error: --file must be provided')
        else:
            rule_synth.synth(auth, args.file)

    parser_rule_synth = subparsers.add_parser('rule-synth')
    parser_rule_synth.set_defaults(run=lambda args: parser_rule_synth.print_help())
    parser_rule_synth_subparsers = parser_rule_synth.add_subparsers()

    parser_synth = parser_rule_synth_subparsers.add_parser('synth')
    parser_synth.add_argument('--file')
    parser_synth.set_defaults(run=rule_synth)

    def cfb_analyze(args):
        if args.job is None:
            print ('error: --job must be provided')
        else:
            if args.path is None:
                print ('error: --path must be provided')
            else:
                cfb.analyze(auth, args.job, args.path)

    parser_cfb = subparsers.add_parser('cfb')
    parser_cfb.set_defaults(run=lambda args: parser_cfb.print_help())
    parser_cfb_subparsers = parser_cfb.add_subparsers()

    parser_cfb_analyze = parser_cfb_subparsers.add_parser('analyze')
    parser_cfb_analyze.add_argument('--job')
    parser_cfb_analyze.add_argument('--path')
    parser_cfb_analyze.set_defaults(run=cfb_analyze)

    def repl(args):
        core.run_repl(auth, args.args)

    parser_repl = parser_core_subparsers.add_parser('repl')
    parser_repl.add_argument('args', nargs=argparse.REMAINDER)
    parser_repl.set_defaults(run=repl)

    def install_imandra_core(args):
        core.install(auth)

    parser_install = parser_core_subparsers.add_parser('install')
    parser_install.set_defaults(run=install_imandra_core)

    if len(sys.argv) > 2 and sys.argv[1] == 'core' and sys.argv[2] == 'repl':
        # Run this directly so we can pass --help directly to the repl command to see its own help text
        core.run_repl(auth, sys.argv[3:])
    else:
        args = parser.parse_args()
        args.run(args)

def session():
    return HttpInstanceSession()