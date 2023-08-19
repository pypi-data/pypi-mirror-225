from pathlib import Path

import batoid
import batoid_rubin
import galsim
import numpy as np


fea_dir = Path(batoid_rubin.datadir) / "fea_legacy"
bend_dir = Path(batoid_rubin.datadir) / "bend_legacy"

zen = 30 * galsim.degrees
rot = 15 * galsim.degrees


def test_fea_nodes_load():
    bx, by, idx1, idx3 = batoid_rubin.builder.m1m3_fea_nodes(fea_dir)
    bx, by = batoid_rubin.builder.m2_fea_nodes(fea_dir)


def test_grid_xy_load():
    m1_grid_xy, m3_grid_xy = batoid_rubin.builder.m1m3_grid_xy(bend_dir)
    m2_grid_xy = batoid_rubin.builder.m2_grid_xy(bend_dir)


def test_fea():
    telescope = batoid.Optic.fromYaml("LSST_r.yaml")
    grav = batoid_rubin.builder.m1m3_gravity(fea_dir, telescope, zen)
    temp = batoid_rubin.builder.m1m3_temperature(fea_dir, 0.0, 0.0, 0.0, 0.0, 0.0)
    lut = batoid_rubin.builder.m1m3_lut(fea_dir, zen, 0.0, 0)

    grav = batoid_rubin.builder.m2_gravity(fea_dir, zen)
    temp = batoid_rubin.builder.m2_temperature(fea_dir, 0.0, 0.0)


def test_load_bend():
    dof = (0,)*20
    m1_bend = batoid_rubin.builder.realize_bend(bend_dir, dof, 0)
    m2_bend = batoid_rubin.builder.realize_bend(bend_dir, dof, 1)
    m3_bend = batoid_rubin.builder.realize_bend(bend_dir, dof, 2)


def test_builder():
    fiducial = batoid.Optic.fromYaml("LSST_r.yaml")
    builder = batoid_rubin.builder.LSSTBuilder(fiducial, fea_dir, bend_dir)
    builder = (
        builder
        .with_m1m3_gravity(zen)
        .with_m1m3_temperature(0.0, 0.1, -0.1, 0.1, 0.1)
        .with_m2_gravity(zen)
        .with_m2_temperature(0.1, 0.1)
        .with_aos_dof(np.array([0]*19+[1]+[0]*30))
        .with_m1m3_lut(zen, 0.0, 0)
        .with_extra_zk([0]*4+[1e-9], 0.61)
    )

    telescope = builder.build()

    # Check that default dirs work
    builder2 = batoid_rubin.LSSTBuilder(fiducial)
    builder2 = (
        builder2
        .with_m1m3_gravity(zen)
        .with_m1m3_temperature(0.0, 0.1, -0.1, 0.1, 0.1)
        .with_m2_gravity(zen)
        .with_m2_temperature(0.1, 0.1)
        .with_aos_dof(np.array([0]*19+[1]+[0]*30))
        .with_m1m3_lut(zen, 0.0, 0)
        .with_extra_zk([0]*4+[1e-9], 0.61)
    )
    telescope2 = builder2.build()
    assert telescope == telescope2

    # Check float interface too.
    builder3 = batoid_rubin.LSSTBuilder(fiducial)
    builder3 = (
        builder3
        .with_m1m3_gravity(zen.rad)
        .with_m1m3_temperature(0.0, 0.1, -0.1, 0.1, 0.1)
        .with_m2_gravity(zen.rad)
        .with_m2_temperature(0.1, 0.1)
        .with_aos_dof(np.array([0]*19+[1]+[0]*30))
        .with_m1m3_lut(zen.rad, 0.0, 0)
        .with_extra_zk([0]*4+[1e-9], 0.61)
    )
    telescope3 = builder3.build()
    assert telescope == telescope3


def test_attr():
    builder = batoid_rubin.LSSTBuilder(batoid.Optic.fromYaml("LSST_r.yaml"))
    assert hasattr(builder.with_m1m3_gravity, "_req_params")


def test_ep_phase():
    fiducial = batoid.Optic.fromYaml("LSST_r.yaml")
    builder = batoid_rubin.builder.LSSTBuilder(fiducial, fea_dir, bend_dir)
    builder = (
        builder
        .with_m1m3_gravity(zen)
        .with_m1m3_temperature(0.0, 0.1, -0.1, 0.1, 0.1)
        .with_m2_gravity(zen)
        .with_m2_temperature(0.1, 0.1)
        .with_aos_dof(np.array([0]*19+[1]+[0]*30))
        .with_m1m3_lut(zen, 0.0, 0)
        .with_extra_zk([0]*4+[1e-9], 0.61)
    )
    telescope = builder.build()
    thx = 0.01
    thy = 0.01
    wavelength=622e-9
    zk = batoid.zernike(
        telescope, thx, thy, wavelength,
        nx=128, jmax=28, eps=0.61
    )
    # Now try to zero-out the wavefront

    builder1 = builder.with_extra_zk(
        zk*wavelength, 0.61
    )
    telescope1 = builder1.build()
    zk1 = batoid.zernike(
        telescope1, thx, thy, wavelength,
        nx=128, jmax=28, eps=0.61
    )

    np.testing.assert_allclose(zk1[4:], 0.0, atol=2e-3)  # 0.002 waves isn't so bad
