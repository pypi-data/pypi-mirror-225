use std::borrow::Borrow;
use std::collections::HashMap;
use std::hash::Hash;
use std::sync::{Arc, Mutex};

pub mod bytes;
pub mod mutable;
pub mod object;
pub mod stream;
pub mod typedef;
pub mod typeinfo;

pub use bytes::*;
pub use mutable::*;
pub use object::*;
pub use stream::*;
pub use typedef::*;
pub use typeinfo::*;

lazy_static::lazy_static! {
    static ref BUILT_IN_TYPES: Arc<Mutex<HashMap<String, Type>>> = {
        let built_ins = HashMap::new();
        Arc::new(Mutex::new(built_ins))
    };
}

/// This function registers a new built-in type. This will allow the registered
/// type to be referenced by name instead of its full type description. This
/// allows for more compressed types. It also reduces the chance of error when
/// working with complex types.
///
/// Note: built-in types that depend on other built-in types should be
/// registered after their dependencies.
pub fn register_built_in(name: String, r#type: Type) {
    let mut mu = BUILT_IN_TYPES.lock().unwrap();
    if mu.get(&name).is_none() {
        mu.insert(name, r#type);
    }
}

/// This function returns the type info for a built-in type. This type should
/// not be used for serialization or deserialization; it should only be used for
/// validation. Serialization or deserialization should be done by using
/// `Type::BuiltIn(name)`.
pub fn built_in<Q>(name: &Q) -> Option<Type>
where
    Q: ?Sized + Hash + Eq,
    String: Borrow<Q>,
{
    BUILT_IN_TYPES.lock().unwrap().get(name).cloned()
}

#[cfg(test)]
mod test {

    use crate::typeinfo::*;

    #[test]
    fn serialize_scalar() {
        let t = Type::Bool;
        let json = serde_json::to_string(&t).unwrap();
        assert_eq!(r#""bool""#, json);
        let t = serde_json::from_str::<Type>(&json).unwrap();
        assert_eq!(t, Type::Bool);

        let t = Type::U8;
        let json = serde_json::to_string(&t).unwrap();
        assert_eq!(r#""u8""#, json);
        let t = serde_json::from_str::<Type>(&json).unwrap();
        assert_eq!(t, Type::U8);

        let t = Type::U16;
        let json = serde_json::to_string(&t).unwrap();
        assert_eq!(r#""u16""#, json);
        let t = serde_json::from_str::<Type>(&json).unwrap();
        assert_eq!(t, Type::U16);

        let t = Type::U32;
        let json = serde_json::to_string(&t).unwrap();
        assert_eq!(r#""u32""#, json);
        let t = serde_json::from_str::<Type>(&json).unwrap();
        assert_eq!(t, Type::U32);

        let t = Type::U64;
        let json = serde_json::to_string(&t).unwrap();
        assert_eq!(r#""u64""#, json);
        let t = serde_json::from_str::<Type>(&json).unwrap();
        assert_eq!(t, Type::U64);

        let t = Type::I8;
        let json = serde_json::to_string(&t).unwrap();
        assert_eq!(r#""i8""#, json);
        let t = serde_json::from_str::<Type>(&json).unwrap();
        assert_eq!(t, Type::I8);

        let t = Type::I16;
        let json = serde_json::to_string(&t).unwrap();
        assert_eq!(r#""i16""#, json);
        let t = serde_json::from_str::<Type>(&json).unwrap();
        assert_eq!(t, Type::I16);

        let t = Type::I32;
        let json = serde_json::to_string(&t).unwrap();
        assert_eq!(r#""i32""#, json);
        let t = serde_json::from_str::<Type>(&json).unwrap();
        assert_eq!(t, Type::I32);

        let t = Type::I64;
        let json = serde_json::to_string(&t).unwrap();
        assert_eq!(r#""i64""#, json);
        let t = serde_json::from_str::<Type>(&json).unwrap();
        assert_eq!(t, Type::I64);

        let t = Type::F32;
        let json = serde_json::to_string(&t).unwrap();
        assert_eq!(r#""f32""#, json);
        let t = serde_json::from_str::<Type>(&json).unwrap();
        assert_eq!(t, Type::F32);

        let t = Type::F64;
        let json = serde_json::to_string(&t).unwrap();
        assert_eq!(r#""f64""#, json);
        let t = serde_json::from_str::<Type>(&json).unwrap();
        assert_eq!(t, Type::F64);

        let t = Type::String;
        let json = serde_json::to_string(&t).unwrap();
        assert_eq!(r#""string""#, json);
        let t = serde_json::from_str::<Type>(&json).unwrap();
        assert_eq!(t, Type::String);
    }

    #[test]
    fn serialize_enum() {
        let t1 = Type::Enum(Enum(vec![
            Variant::Tagged("Foo".to_string()),
            Variant::TaggedFields(
                "Bar".to_string(),
                Fields::Unnamed(vec![
                    Type::I32,
                    Type::F32,
                    Type::String,
                    Type::Tuple(Tuple(vec![Type::I32, Type::F32, Type::String])),
                ]),
            ),
            Variant::TaggedFields(
                "Baz".to_string(),
                Fields::Named(
                    [
                        ("i".to_string(), Type::I32),
                        ("f".to_string(), Type::F32),
                        ("s".to_string(), Type::String),
                        (
                            "t".to_string(),
                            Type::Tuple(Tuple(vec![Type::I32, Type::F32, Type::String])),
                        ),
                    ]
                    .into_iter()
                    .collect(),
                ),
            ),
        ]));

        let json = serde_json::to_string(&t1).unwrap();
        assert_eq!(
            r#"{"k":"enum","t":["Foo",{"Bar":["i32","f32","string",{"k":"tuple","t":["i32","f32","string"]}]},{"Baz":{"f":"f32","i":"i32","s":"string","t":{"k":"tuple","t":["i32","f32","string"]}}}]}"#,
            json
        );

        let t2 = serde_json::from_str::<Type>(&json).unwrap();
        assert_eq!(t1, t2);
    }
}
