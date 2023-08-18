use crate::rcsb::compare_and_check_bonds;
use qdx_common::AtomCheckStrictness;

#[test]
fn load_and_fix_pdb1vcb() -> anyhow::Result<()> {
    compare_and_check_bonds("data/rcsb/vhl/1vcb.pdb", 1, AtomCheckStrictness::None)?;

    Ok(())
}

#[test]
fn load_and_fix_pdb1za8() -> anyhow::Result<()> {
    compare_and_check_bonds("data/rcsb/vhl/1za8.pdb", 20, AtomCheckStrictness::Heavy)?;
    Ok(())
}

#[test]
fn load_and_fix_pdb2kuk() -> anyhow::Result<()> {
    compare_and_check_bonds("data/rcsb/vhl/2kuk.pdb", 20, AtomCheckStrictness::Heavy)?;

    Ok(())
}
