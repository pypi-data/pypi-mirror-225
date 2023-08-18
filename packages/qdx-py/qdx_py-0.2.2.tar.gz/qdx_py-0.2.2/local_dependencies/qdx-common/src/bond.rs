use qdx_derive::Typedef;

pub type BondOrder = u8;

pub const BOND_ORDER_SINGLE: BondOrder = 1;
pub const BOND_ORDER_DOUBLE: BondOrder = 2;
pub const BOND_ORDER_TRIPLE: BondOrder = 3;
pub const BOND_ORDER_ONEANDAHALF: BondOrder = 254;
pub const BOND_ORDER_RING: BondOrder = 255;

/// A bond represents a connection between 2 atoms. The first 2 elements of the
/// tuple are the indices of the conencted atoms. The last element of the tuple
/// is the bond order of the connection.
#[derive(Clone, Copy, Debug, Eq, PartialEq, PartialOrd, Ord, Typedef)]
#[cfg_attr(feature = "serde", derive(::serde::Deserialize, ::serde::Serialize))]
pub struct Bond(pub u32, pub u32, pub BondOrder);

#[cfg(feature = "graphql")]
async_graphql::scalar!(Bond);

/// BondOrder, MinDistance, MaxDistance
type BondInfo = (BondOrder, f32, f32);

type Orders<'a> = Vec<(&'a str, &'a str, Vec<BondInfo>)>;

/// Experimentally verified distances of various bonds and bond orders.
pub struct BondOrders<'a> {
    /// Bonds and bond orders are stored as a Vec<(Symbol, Symbol, Vec<BondInfo>)>
    pub orders: Orders<'a>,
}

impl Default for BondOrders<'_> {
    fn default() -> Self {
        Self {
            orders: vec![
                ("C", "BR", vec![(1, 1.789, 1.95)]),
                (
                    "C",
                    "C",
                    vec![
                        (1, 1.37, 1.725),
                        (2, 1.243, 1.382),
                        (3, 1.187, 1.268),
                        (BOND_ORDER_RING, 1.37, 1.432),
                    ],
                ),
                ("C", "CA", vec![(3, 2.295, 2.305)]),
                ("C", "CL", vec![(1, 1.612, 1.813)]),
                ("C", "F", vec![(1, 1.262, 1.401)]),
                ("C", "H", vec![(1, 0.931, 1.14)]),
                ("C", "I", vec![(1, 1.992, 2.157)]),
                (
                    "C",
                    "N",
                    vec![
                        (1, 1.347, 1.569),
                        (2, 1.207, 1.332),
                        (3, 1.14, 1.177),
                        (BOND_ORDER_RING, 1.328, 1.35),
                    ],
                ),
                (
                    "C",
                    "O",
                    vec![(1, 1.32, 1.5), (2, 1.146, 1.272), (3, 1.128, 1.145)],
                ),
                (
                    "C",
                    "P",
                    vec![(1, 1.858, 1.858), (2, 1.673, 1.673), (3, 1.542, 1.562)],
                ),
                (
                    "C",
                    "S",
                    vec![(1, 1.714, 1.863), (2, 1.553, 1.647), (3, 1.478, 1.535)],
                ),
                ("C", "SE", vec![(1, 1.855, 1.959), (2, 1.676, 1.709)]),
                ("C", "SI", vec![(1, 1.722, 1.848)]),
                ("CA", "H", vec![(1, 2.000, 2.005)]),
                ("CA", "O", vec![(1, 1.81, 1.976)]),
                ("CA", "S", vec![(2, 2.250, 2.350)]),
                ("CL", "CL", vec![(1, 1.9879, 1.9879)]),
                ("CL", "S", vec![(1, 1.975, 2.07)]),
                ("F", "F", vec![(1, 1.322, 1.412)]),
                ("F", "S", vec![(1, 1.530, 1.643)]),
                ("F", "O", vec![(1, 1.421, 1.421)]),
                ("F", "CL", vec![(1, 1.597, 1.713)]),
                ("FE", "N", vec![(1, 1.98, 2.64)]),
                ("H", "CL", vec![(1, 1.275, 1.321)]),
                ("H", "F", vec![(1, 0.917, 1.014)]),
                ("H", "H", vec![(1, 0.741, 0.741)]),
                ("H", "P", vec![(1, 1.399, 1.399)]),
                // FIXME: Not based on experimental data
                ("N", "CA", vec![(1, 2.295, 2.305)]),
                ("N", "CL", vec![(1, 1.611, 1.975)]),
                ("N", "F", vec![(1, 1.317, 1.512)]),
                ("N", "H", vec![(1, 0.836, 1.09)]),
                (
                    "N",
                    "N",
                    vec![
                        (1, 1.181, 1.864),
                        (2, 1.139, 1.252),
                        (3, 1.098, 1.133),
                        (BOND_ORDER_RING, 1.332, 1.332),
                    ],
                ),
                ("N", "O", vec![(1, 1.184, 1.507), (2, 1.066, 1.258)]),
                ("N", "P", vec![(3, 1.481, 1.501)]),
                ("N", "S", vec![(1, 1.44, 1.719), (3, 1.448, 1.448)]),
                ("O", "CL", vec![(1, 1.641, 1.704), (2, 1.404, 1.414)]),
                ("O", "H", vec![(1, 0.912, 1.033)]),
                ("O", "O", vec![(1, 1.116, 1.516), (2, 1.2, 1.208)]),
                ("O", "S", vec![(2, 1.405, 1.5)]),
                ("O", "P", vec![(1, 1.54, 1.54), (2, 1.436, 1.512)]),
                ("S", "H", vec![(1, 1.322, 1.4)]),
                ("S", "S", vec![(1, 1.89, 2.155), (2, 1.825, 1.898)]),
            ],
        }
    }
}

impl BondOrders<'_> {
    /// Get the maximum bond order based on the atom element symbols and the
    /// distance (in Ångstroms). The tolerance allows the distance to be within
    /// some error of the experimentally measured values. Ring bonds are
    /// returned as BOND_ORDER_RING.
    ///
    /// # Example
    /// ```
    /// use qdx_common::bond::BondOrders;
    /// let orders = BondOrders::default();
    /// let order = orders.max_bond_order("C", "H", 1.0, 0.05);
    /// assert_eq!(order, Some(1))
    /// ```
    pub fn max_bond_order(
        &self,
        e1: &str,
        e2: &str,
        dist: f32,
        tolerance: f32,
    ) -> Option<BondOrder> {
        self.orders
            .iter()
            .find(|(oe1, oe2, _)| (*oe1 == e1 && *oe2 == e2) || (*oe1 == e2 && *oe2 == e1))
            .map(|(_, _, orders)| {
                // bond is within experimentally validated lengths
                let good_matches = orders
                    .iter()
                    .filter_map(|(order, min, max)| {
                        if *min <= dist + tolerance && dist - tolerance <= *max {
                            Some(*order)
                        } else {
                            None
                        }
                    })
                    .max()
                    .unwrap_or(0);

                // bond might still exist - it's valid as long as it's smaller than the largest known distance
                if good_matches == 0 {
                    orders
                        .iter()
                        .filter_map(
                            |(order, min, _max)| {
                                if dist <= *min {
                                    Some(*order)
                                } else {
                                    None
                                }
                            },
                        )
                        .max()
                        .unwrap_or(0)
                } else {
                    good_matches
                }
            })
    }
}

/// Utility for keeping track of how to assign aromatic ring bond orders
pub struct RingResolver {
    on: bool,
}

impl Default for RingResolver {
    fn default() -> Self {
        Self::new()
    }
}

impl RingResolver {
    pub fn new() -> Self {
        Self { on: true }
    }

    /// Bonds in aromatic rings are represented with an order of
    /// RING_BOND_ORDER. To resolve this accurately, we alternate bond orders
    /// (e.g. 1-2-1-2-1-2) starting from 1.
    /// TODO: There might be heuristics that we are missing for whether or not
    /// to start the ring stepping with bond order 1 or 2.
    pub fn step(&mut self, val: BondOrder) -> BondOrder {
        if val != BOND_ORDER_RING {
            return val;
        }
        if self.on {
            self.on = false;
            2
        } else {
            self.on = true;
            1
        }
    }
}
