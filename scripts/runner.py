#!/usr/bin/env python

from lammps import lammps
import os
import argparse

parser = argparse.ArgumentParser(description='Run LAMMPS simulation with an input file')
parser.add_argument('-i', '--input')
parser.add_argument('--resume')
parser.add_argument('--resett', default=False, action='store_true')
parser.add_argument('-o', '--out')
parser.add_argument('-e', '--every', type=int)
parser.add_argument('-n', '--nsteps', type=int)
args = parser.parse_args()

lmp = lammps()

lmp.command('read_restart {}'.format(args.resume))
if args.resett:
    lmp.command('reset_timestep  0')

lmp.file(args.input)

if os.path.exists('{}.conf'.format(args.out)):
    dopt = raw_input('Configuration file exists, (o)verwrite, (l)eave, (c)ancel?')
    if dopt == 'o':
        conf_write = True
    elif dopt == 'l':
        conf_write = False
    else:
        raise Exception('Cancelled by user')
if conf_write:
    lmp.file('write_restart {}.conf'.format(args.out))

lmp.file('run {}'.format(args.n))

if os.path.exists('{}.dump'.format(args.out)):
    copt = raw_input('Dump file exists, (o)verwrite, (a)ppend, (l)eave, (c)ancel?')
    if copt == 'o':
        dump_write = True
    elif copt == 'l':
        dump_write = False
    elif copt == 'a':
        dump_write = True
        dump_append = True
    else:
        raise Exception('Cancelled by user')
if dump_write:
    lmp.file('dump 1 all custom {} {}.dump id type x y z fx fy fz v_f_prop_x v_f_prop_y v_f_prop_z f_f_cons[1] f_f_cons[2] f_f_cons[3] tqx tqy tqz'.format(args.every, args.out))
    if dump_append:
        lmp.file('dump_modify 1 append yes buffer yes')
