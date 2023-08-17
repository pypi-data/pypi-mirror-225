use qdx_common::*;

#[test]
fn test_topology_creation() {
    init_built_in_types();
    let topology = Topology {
        symbols: vec!["C".into(), "H".into(), "O".into()],
        geometry: vec![1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0],
        atom_charges: Some(vec![0, 0, 0]),
        partial_charges: None,
        atom_labels: None,
        alts: None,
        connectivity: None,
        fragments: Some(vec![vec![0], vec![1], vec![2]]),
        fragment_charges: Some(vec![0, 0, 0]),
    };
    assert_eq!(topology.symbols.len(), 3);
    assert_eq!(topology.symbols, vec!["C", "H", "O"]);
    assert_eq!(topology.geometry.len(), 9);
    assert_eq!(
        topology.geometry,
        vec![1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0]
    );
    assert!(topology.is_valid());
}

#[test]
fn test_topology_drop_atoms() {
    init_built_in_types();
    let mut topology = Topology {
        symbols: vec!["Cl".into(), "Cl".into(), "Cl".into()],
        geometry: vec![1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0],
        atom_charges: Some(vec![-1, -1, -1]),
        partial_charges: None,
        atom_labels: None,
        alts: None,
        connectivity: None,
        fragments: Some(vec![vec![0, 1, 2]]),
        fragment_charges: Some(vec![-3]),
    };
    assert_eq!(topology.symbols.len(), 3);
    assert_eq!(topology.symbols, vec!["Cl", "Cl", "Cl"]);
    assert_eq!(topology.geometry.len(), 9);
    assert_eq!(
        topology.geometry,
        vec![1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0]
    );
    assert_eq!(topology.atom_charges.as_ref().unwrap().len(), 3);
    assert_eq!(topology.atom_charges.as_ref().unwrap(), &vec![-1, -1, -1]);
    assert_eq!(topology.fragments.as_ref().unwrap().len(), 1);
    assert_eq!(topology.fragments.as_ref().unwrap(), &vec![vec![0, 1, 2]]);
    assert_eq!(topology.fragment_charges.as_ref().unwrap().len(), 1);
    assert_eq!(topology.fragment_charges.as_ref().unwrap(), &vec![-3]);
    topology.drop_atoms(&[0]);
    assert_eq!(topology.symbols.len(), 2);
    assert_eq!(topology.symbols, vec!["Cl", "Cl"]);
    assert_eq!(topology.geometry.len(), 6);
    assert_eq!(topology.geometry, vec![2.0, 2.0, 2.0, 3.0, 3.0, 3.0]);
    assert_eq!(topology.atom_charges.as_ref().unwrap().len(), 2);
    assert_eq!(topology.atom_charges.as_ref().unwrap(), &vec![-1, -1]);
    assert_eq!(topology.fragments.as_ref().unwrap().len(), 1);
    assert_eq!(topology.fragments.as_ref().unwrap(), &vec![vec![0, 1]]);
    assert_eq!(topology.fragment_charges.as_ref().unwrap().len(), 1);
    assert_eq!(topology.fragment_charges.as_ref().unwrap(), &vec![-2]);
    assert!(topology.is_valid());
}

#[test]
fn test_topology_drop_fragments() {
    init_built_in_types();
    let mut topology = Topology {
        symbols: vec!["Cl".into(), "Cl".into(), "Cl".into()],
        geometry: vec![1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0],
        atom_charges: Some(vec![-1, -1, -1]),
        partial_charges: None,
        atom_labels: None,
        alts: None,
        connectivity: None,
        fragments: Some(vec![vec![0, 1], vec![2]]),
        fragment_charges: Some(vec![-2, -1]),
    };
    topology.drop_fragments(&[0]);
    assert_eq!(topology.symbols.len(), 1);
    assert_eq!(topology.symbols, vec!["Cl"]);
    assert_eq!(topology.geometry.len(), 3);
    assert_eq!(topology.geometry, vec![3.0, 3.0, 3.0]);
    assert_eq!(topology.atom_charges.as_ref().unwrap().len(), 1);
    assert_eq!(topology.atom_charges.as_ref().unwrap(), &(vec![-1]));
    assert_eq!(topology.fragments.as_ref().unwrap().len(), 1);
    assert_eq!(topology.fragments.as_ref().unwrap(), &(vec![vec![0]]));
    assert_eq!(topology.fragment_charges.as_ref().unwrap().len(), 1);
    assert_eq!(topology.fragment_charges.as_ref().unwrap(), &(vec![-1]));
    assert!(topology.is_valid());
}
