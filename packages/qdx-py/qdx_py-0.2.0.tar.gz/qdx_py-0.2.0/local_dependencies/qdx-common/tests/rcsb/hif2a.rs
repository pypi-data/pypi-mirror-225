use crate::rcsb::compare_and_check_bonds;
use qdx_common::AtomCheckStrictness;

#[test]
fn load_and_fix_pdb1p97() -> anyhow::Result<()> {
    compare_and_check_bonds("data/rcsb/hif2a/1p97.pdb", 20, AtomCheckStrictness::Heavy)?;
    Ok(())
}

#[test]
fn load_and_fix_pdb6czw() -> anyhow::Result<()> {
    compare_and_check_bonds("data/rcsb/hif2a/6czw.pdb", 1, AtomCheckStrictness::Heavy)?;
    Ok(())
}

#[test]
fn load_and_fix_pdb6d09() -> anyhow::Result<()> {
    compare_and_check_bonds("data/rcsb/hif2a/6d09.pdb", 1, AtomCheckStrictness::Heavy)?;
    Ok(())
}

#[test]
fn load_and_fix_pdb6d0b() -> anyhow::Result<()> {
    compare_and_check_bonds("data/rcsb/hif2a/6d0b.pdb", 1, AtomCheckStrictness::Heavy)?;
    Ok(())
}

#[test]
fn load_and_fix_pdb6d0c() -> anyhow::Result<()> {
    compare_and_check_bonds("data/rcsb/hif2a/6d0c.pdb", 1, AtomCheckStrictness::Heavy)?;
    Ok(())
}

#[test]
fn load_and_fix_pdb6x21() -> anyhow::Result<()> {
    compare_and_check_bonds("data/rcsb/hif2a/6x21.pdb", 1, AtomCheckStrictness::Heavy)?;
    Ok(())
}

#[test]
fn load_and_fix_pdb6x2h() -> anyhow::Result<()> {
    compare_and_check_bonds("data/rcsb/hif2a/6x2h.pdb", 1, AtomCheckStrictness::Heavy)?;
    Ok(())
}

#[test]
fn load_and_fix_pdb6x37() -> anyhow::Result<()> {
    compare_and_check_bonds("data/rcsb/hif2a/6x37.pdb", 1, AtomCheckStrictness::Heavy)?;
    Ok(())
}

#[test]
fn load_and_fix_pdb6x3d() -> anyhow::Result<()> {
    compare_and_check_bonds("data/rcsb/hif2a/6x3d.pdb", 1, AtomCheckStrictness::Heavy)?;
    Ok(())
}

#[test]
fn load_and_fix_pdb7ujv() -> anyhow::Result<()> {
    compare_and_check_bonds("data/rcsb/hif2a/7ujv.pdb", 1, AtomCheckStrictness::Heavy)?;
    Ok(())
}
