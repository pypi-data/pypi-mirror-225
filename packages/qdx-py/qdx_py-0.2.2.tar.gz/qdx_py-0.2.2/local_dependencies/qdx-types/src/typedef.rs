use crate::{typeinfo::Type, Array, Optional, Tuple};

pub trait Typedef {
    fn describe() -> Type;
}

impl Typedef for () {
    fn describe() -> Type {
        Type::Unit
    }
}

impl Typedef for bool {
    fn describe() -> Type {
        Type::Bool
    }
}

impl Typedef for u8 {
    fn describe() -> Type {
        Type::U8
    }
}

impl Typedef for u16 {
    fn describe() -> Type {
        Type::U16
    }
}

impl Typedef for u32 {
    fn describe() -> Type {
        Type::U32
    }
}

impl Typedef for u64 {
    fn describe() -> Type {
        Type::U64
    }
}

impl Typedef for i8 {
    fn describe() -> Type {
        Type::I8
    }
}

impl Typedef for i16 {
    fn describe() -> Type {
        Type::I16
    }
}

impl Typedef for i32 {
    fn describe() -> Type {
        Type::I32
    }
}

impl Typedef for i64 {
    fn describe() -> Type {
        Type::I64
    }
}

impl Typedef for f32 {
    fn describe() -> Type {
        Type::F32
    }
}

impl Typedef for f64 {
    fn describe() -> Type {
        Type::F64
    }
}

impl Typedef for String {
    fn describe() -> Type {
        Type::String
    }
}

impl<T> Typedef for Option<T>
where
    T: Typedef,
{
    fn describe() -> Type {
        Type::Optional(Optional(Box::new(T::describe())))
    }
}

impl<T> Typedef for Vec<T>
where
    T: Typedef,
{
    fn describe() -> Type {
        Type::Array(Array(Box::new(T::describe())))
    }
}

impl<T> Typedef for (T,)
where
    T: Typedef,
{
    fn describe() -> Type {
        Type::Tuple(Tuple(vec![T::describe()]))
    }
}

impl<T0, T1> Typedef for (T0, T1)
where
    T0: Typedef,
    T1: Typedef,
{
    fn describe() -> Type {
        Type::Tuple(Tuple(vec![T0::describe(), T1::describe()]))
    }
}

impl<T0, T1, T2> Typedef for (T0, T1, T2)
where
    T0: Typedef,
    T1: Typedef,
    T2: Typedef,
{
    fn describe() -> Type {
        Type::Tuple(Tuple(vec![T0::describe(), T1::describe(), T2::describe()]))
    }
}

impl<T0, T1, T2, T3> Typedef for (T0, T1, T2, T3)
where
    T0: Typedef,
    T1: Typedef,
    T2: Typedef,
    T3: Typedef,
{
    fn describe() -> Type {
        Type::Tuple(Tuple(vec![
            T0::describe(),
            T1::describe(),
            T2::describe(),
            T3::describe(),
        ]))
    }
}

impl<T0, T1, T2, T3, T4> Typedef for (T0, T1, T2, T3, T4)
where
    T0: Typedef,
    T1: Typedef,
    T2: Typedef,
    T3: Typedef,
    T4: Typedef,
{
    fn describe() -> Type {
        Type::Tuple(Tuple(vec![
            T0::describe(),
            T1::describe(),
            T2::describe(),
            T3::describe(),
            T4::describe(),
        ]))
    }
}

impl<T0, T1, T2, T3, T4, T5> Typedef for (T0, T1, T2, T3, T4, T5)
where
    T0: Typedef,
    T1: Typedef,
    T2: Typedef,
    T3: Typedef,
    T4: Typedef,
    T5: Typedef,
{
    fn describe() -> Type {
        Type::Tuple(Tuple(vec![
            T0::describe(),
            T1::describe(),
            T2::describe(),
            T3::describe(),
            T4::describe(),
            T5::describe(),
        ]))
    }
}

impl<T0, T1, T2, T3, T4, T5, T6> Typedef for (T0, T1, T2, T3, T4, T5, T6)
where
    T0: Typedef,
    T1: Typedef,
    T2: Typedef,
    T3: Typedef,
    T4: Typedef,
    T5: Typedef,
    T6: Typedef,
{
    fn describe() -> Type {
        Type::Tuple(Tuple(vec![
            T0::describe(),
            T1::describe(),
            T2::describe(),
            T3::describe(),
            T4::describe(),
            T5::describe(),
            T6::describe(),
        ]))
    }
}

impl<T0, T1, T2, T3, T4, T5, T6, T7> Typedef for (T0, T1, T2, T3, T4, T5, T6, T7)
where
    T0: Typedef,
    T1: Typedef,
    T2: Typedef,
    T3: Typedef,
    T4: Typedef,
    T5: Typedef,
    T6: Typedef,
    T7: Typedef,
{
    fn describe() -> Type {
        Type::Tuple(Tuple(vec![
            T0::describe(),
            T1::describe(),
            T2::describe(),
            T3::describe(),
            T4::describe(),
            T5::describe(),
            T6::describe(),
            T7::describe(),
        ]))
    }
}
