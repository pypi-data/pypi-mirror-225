use std::{
    collections::BTreeMap,
    fmt::{self, Display, Formatter},
};

#[cfg(feature = "serde")]
use serde::{
    de::{self, MapAccess, SeqAccess, Visitor},
    ser::{Error, SerializeMap},
    Deserialize, Deserializer, Serialize, Serializer,
};
#[cfg(feature = "sqlx")]
use sqlx::{
    database::{HasArguments, HasValueRef},
    encode::IsNull,
    postgres::PgHasArrayType,
    Database, Decode, Encode, Postgres,
};

use crate::built_in;

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum Type {
    Unit,
    Bool,
    U8,
    U16,
    U32,
    U64,
    I8,
    I16,
    I32,
    I64,
    F32,
    F64,
    String,
    Bytes,

    Optional(Optional),
    Array(Array),
    Tuple(Tuple),
    Record(Record),
    Enum(Enum),
    Func(Func),

    Object(Box<Type>),
    Stream(Box<Type>),
    BuiltIn(String),
}

impl Display for Type {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Type::Unit => '_'.fmt(f),
            Type::Bool => "bool".fmt(f),
            Type::U8 => "u8".fmt(f),
            Type::U16 => "u16".fmt(f),
            Type::U32 => "u32".fmt(f),
            Type::U64 => "u64".fmt(f),
            Type::I8 => "i8".fmt(f),
            Type::I16 => "i16".fmt(f),
            Type::I32 => "i32".fmt(f),
            Type::I64 => "i64".fmt(f),
            Type::F32 => "f32".fmt(f),
            Type::F64 => "f64".fmt(f),
            Type::String => "string".fmt(f),
            Type::Bytes => "bytes".fmt(f),

            Type::Optional(inner) => inner.fmt(f),
            Type::Array(inner) => inner.fmt(f),
            Type::Tuple(inner) => inner.fmt(f),
            Type::Record(inner) => inner.fmt(f),
            Type::Enum(inner) => inner.fmt(f),
            Type::Func(inner) => inner.fmt(f),

            Type::Object(t) => {
                '@'.fmt(f)?;
                t.fmt(f)
            }
            Type::Stream(t) => {
                '~'.fmt(f)?;
                t.fmt(f)
            }
            Type::BuiltIn(n) => n.fmt(f),
        }
    }
}

/// Optional defines the type for a value that is possibly null.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Optional(pub Box<Type>);

impl Display for Optional {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        self.0.fmt(f)?;
        '?'.fmt(f)
    }
}

/// Array defines an ordered set of homogeneously typed values.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Array(pub Box<Type>);

impl Display for Array {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        '['.fmt(f)?;
        self.0.fmt(f)?;
        ']'.fmt(f)
    }
}

/// Tuple defines an algebraic product type of unnamed heterogeneously typed
/// values.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Tuple(pub Vec<Type>);

impl Display for Tuple {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        '('.fmt(f)?;
        let mut first = true;
        for t in &self.0 {
            if first {
                first = false;
            } else {
                ','.fmt(f)?;
            }
            t.fmt(f)?;
        }
        ')'.fmt(f)
    }
}

/// Record defines an algebraic product type of named heterogeneously typed
/// values.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Record(pub BTreeMap<String, Type>);

impl Display for Record {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        '{'.fmt(f)?;
        let mut first = true;
        for (k, t) in &self.0 {
            if first {
                first = false;
            } else {
                ','.fmt(f)?;
            }
            k.fmt(f)?;
            ':'.fmt(f)?;
            t.fmt(f)?;
        }
        '}'.fmt(f)
    }
}

/// Record defines tagged union of heterogeneously typed variants.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Enum(pub Vec<Variant>);

impl Display for Enum {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        let mut first = true;
        for v in &self.0 {
            if first {
                first = false;
            } else {
                '|'.fmt(f)?;
            }
            v.fmt(f)?;
        }
        Ok(())
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum Variant {
    Tagged(String),
    TaggedFields(String, Fields),
}

impl Display for Variant {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Variant::Tagged(s) => s.fmt(f),
            Variant::TaggedFields(s, fields) => {
                s.fmt(f)?;
                fields.fmt(f)
            }
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum Fields {
    Unnamed(Vec<Type>),
    Named(BTreeMap<String, Type>),
}

impl Display for Fields {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Fields::Unnamed(t) => {
                '('.fmt(f)?;
                let mut first = true;
                for t in t {
                    if first {
                        first = false;
                    } else {
                        ','.fmt(f)?;
                    }
                    t.fmt(f)?;
                }
                ')'.fmt(f)
            }
            Fields::Named(t) => {
                '{'.fmt(f)?;
                let mut first = true;
                for (k, t) in t {
                    if first {
                        first = false;
                    } else {
                        ','.fmt(f)?;
                    }
                    k.fmt(f)?;
                    ':'.fmt(f)?;
                    t.fmt(f)?;
                }
                '}'.fmt(f)
            }
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Func(pub Vec<Type>, pub Vec<Type>);

impl Display for Func {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        '('.fmt(f)?;
        let mut first = true;
        for t in &self.0 {
            if first {
                first = false;
            } else {
                ','.fmt(f)?;
            }
            t.fmt(f)?;
        }

        ')'.fmt(f)?;
        " -> ".fmt(f)?;

        if self.1.len() > 1 {
            '('.fmt(f)?;
        }
        let mut first = true;
        for t in &self.1 {
            if first {
                first = false;
            } else {
                ','.fmt(f)?;
            }
            t.fmt(f)?;
        }
        if self.1.len() > 1 {
            ')'.fmt(f)?;
        }

        Ok(())
    }
}

#[cfg(feature = "serde")]
impl Serialize for Optional {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let mut map = serializer.serialize_map(Some(2))?;
        map.serialize_entry("k", "optional")?;
        map.serialize_entry("t", &self.0)?;
        map.end()
    }
}

#[cfg(feature = "serde")]
impl Serialize for Array {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let mut map = serializer.serialize_map(Some(2))?;
        map.serialize_entry("k", "array")?;
        map.serialize_entry("t", &self.0)?;
        map.end()
    }
}

#[cfg(feature = "serde")]
impl Serialize for Tuple {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let mut map = serializer.serialize_map(Some(2))?;
        map.serialize_entry("k", "tuple")?;
        map.serialize_entry("t", &self.0)?;
        map.end()
    }
}

#[cfg(feature = "serde")]
impl Serialize for Record {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let mut map = serializer.serialize_map(Some(2))?;
        map.serialize_entry("k", "record")?;
        map.serialize_entry("t", &self.0)?;
        map.end()
    }
}

#[cfg(feature = "serde")]
impl Serialize for Enum {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let mut map = serializer.serialize_map(Some(2))?;
        map.serialize_entry("k", "enum")?;
        map.serialize_entry("t", &self.0)?;
        map.end()
    }
}

#[cfg(feature = "serde")]
struct VariantVisitor;

#[cfg(feature = "serde")]
impl<'de> Visitor<'de> for VariantVisitor {
    type Value = Variant;

    fn expecting(&self, formatter: &mut Formatter) -> fmt::Result {
        formatter.write_str("enum variant")
    }

    fn visit_str<E>(self, value: &str) -> Result<Self::Value, E>
    where
        E: de::Error,
    {
        Ok(Variant::Tagged(value.to_string()))
    }

    fn visit_map<M>(self, mut access: M) -> Result<Self::Value, M::Error>
    where
        M: MapAccess<'de>,
    {
        use serde::de::Error;

        match access.next_key::<String>()? {
            Some(tag) => access
                .next_value::<Fields>()
                .map(|fields| Variant::TaggedFields(tag, fields)),
            _ => Err(M::Error::custom("expected `tag`")),
        }
    }
}

#[cfg(feature = "serde")]
impl<'de> Deserialize<'de> for Variant {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        deserializer.deserialize_any(VariantVisitor)
    }
}

#[cfg(feature = "serde")]
impl Serialize for Variant {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match self {
            Self::Tagged(tag) => tag.serialize(serializer),
            Self::TaggedFields(tag, fields) => {
                let mut map = serializer.serialize_map(Some(2))?;
                map.serialize_entry(tag, fields)?;
                map.end()
            }
        }
    }
}

#[cfg(feature = "serde")]
struct FieldsVisitor;

#[cfg(feature = "serde")]
impl<'de> Visitor<'de> for FieldsVisitor {
    type Value = Fields;

    fn expecting(&self, formatter: &mut Formatter) -> fmt::Result {
        formatter.write_str("enum variant fields")
    }

    fn visit_map<M>(self, mut access: M) -> Result<Self::Value, M::Error>
    where
        M: MapAccess<'de>,
    {
        let mut fields = BTreeMap::new();
        while let Some(field) = access.next_key::<String>()? {
            fields.insert(field, access.next_value::<Type>()?);
        }
        Ok(Fields::Named(fields))
    }

    fn visit_seq<M>(self, mut access: M) -> Result<Self::Value, M::Error>
    where
        M: SeqAccess<'de>,
    {
        let mut fields = Vec::new();
        while let Some(t) = access.next_element::<Type>()? {
            fields.push(t);
        }
        Ok(Fields::Unnamed(fields))
    }
}

#[cfg(feature = "serde")]
impl<'de> Deserialize<'de> for Fields {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        deserializer.deserialize_any(FieldsVisitor)
    }
}

#[cfg(feature = "serde")]
impl Serialize for Fields {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match self {
            Self::Unnamed(fields) => fields.serialize(serializer),
            Self::Named(fields) => fields.serialize(serializer),
        }
    }
}

#[cfg(feature = "serde")]
impl Serialize for Func {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let mut map = serializer.serialize_map(Some(2))?;
        map.serialize_entry("k", "func")?;
        map.serialize_entry("t", &(&self.0, &self.1))?;
        map.end()
    }
}

#[cfg(feature = "serde")]
pub struct TypeVisitor;

#[cfg(feature = "serde")]
impl<'de> Visitor<'de> for TypeVisitor {
    type Value = Type;

    fn expecting(&self, formatter: &mut Formatter) -> fmt::Result {
        formatter.write_str("valid type description")
    }

    fn visit_str<E>(self, value: &str) -> Result<Self::Value, E>
    where
        E: de::Error,
    {
        match value {
            "_" => Ok(Type::Unit),
            "bool" => Ok(Type::Bool),
            "u8" => Ok(Type::U8),
            "u16" => Ok(Type::U16),
            "u32" => Ok(Type::U32),
            "u64" => Ok(Type::U64),
            "i8" => Ok(Type::I8),
            "i16" => Ok(Type::I16),
            "i32" => Ok(Type::I32),
            "i64" => Ok(Type::I64),
            "f32" => Ok(Type::F32),
            "f64" => Ok(Type::F64),
            "string" => Ok(Type::String),
            "bytes" => Ok(Type::Bytes),
            x => match built_in(x) {
                Some(_t) => Ok(Type::BuiltIn(x.to_string())),
                _ => Err(E::custom(format!("unrecognized scalar type {value}"))),
            },
        }
    }

    fn visit_map<M>(self, mut access: M) -> Result<Self::Value, M::Error>
    where
        M: MapAccess<'de>,
    {
        let k_key = access.next_key::<String>()?;
        if k_key.map(|k| k != "k").unwrap_or(true) {
            return Err(de::Error::custom("expected `k`"));
        }
        let k_value = access.next_value::<String>()?;

        let t_key = access.next_key::<String>()?;
        if t_key.map(|t| t != "t").unwrap_or(true) {
            return Err(de::Error::custom("expected `t`"));
        }

        match k_value.as_str() {
            "optional" => Ok(Type::Optional(Optional(Box::new(
                access.next_value::<Type>()?,
            )))),
            "array" => Ok(Type::Array(Array(Box::new(access.next_value::<Type>()?)))),
            "tuple" => Ok(Type::Tuple(Tuple(access.next_value::<Vec<Type>>()?))),
            "record" => Ok(Type::Record(Record(
                access.next_value::<BTreeMap<String, Type>>()?,
            ))),
            "enum" => Ok(Type::Enum(Enum(access.next_value::<Vec<Variant>>()?))),
            "func" => Ok(Type::Func(Func(
                access.next_value::<Vec<Type>>()?,
                access.next_value::<Vec<Type>>()?,
            ))),
            "object" => Ok(Type::Object(Box::new(access.next_value::<Type>()?))),
            "stream" => Ok(Type::Stream(Box::new(access.next_value::<Type>()?))),
            _ => Err(de::Error::custom(format!("unexpected type `{k_value}`"))),
        }
    }
}

#[cfg(feature = "serde")]
impl<'de> Deserialize<'de> for Type {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        deserializer.deserialize_any(TypeVisitor)
    }
}

#[cfg(feature = "serde")]
impl Serialize for Type {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match self {
            Self::Unit => serializer.serialize_str("_"),
            Self::Bool => serializer.serialize_str("bool"),
            Self::U8 => serializer.serialize_str("u8"),
            Self::U16 => serializer.serialize_str("u16"),
            Self::U32 => serializer.serialize_str("u32"),
            Self::U64 => serializer.serialize_str("u64"),
            Self::I8 => serializer.serialize_str("i8"),
            Self::I16 => serializer.serialize_str("i16"),
            Self::I32 => serializer.serialize_str("i32"),
            Self::I64 => serializer.serialize_str("i64"),
            Self::F32 => serializer.serialize_str("f32"),
            Self::F64 => serializer.serialize_str("f64"),
            Self::String => serializer.serialize_str("string"),
            Self::Bytes => serializer.serialize_str("bytes"),

            Self::Optional(optional) => optional.serialize(serializer),
            Self::Array(array) => array.serialize(serializer),
            Self::Tuple(tuple) => tuple.serialize(serializer),
            Self::Record(fields) => fields.serialize(serializer),
            Self::Enum(variants) => variants.serialize(serializer),
            Self::Func(func) => func.serialize(serializer),

            Self::Object(t) => {
                let mut map = serializer.serialize_map(Some(2))?;
                map.serialize_entry("k", "object")?;
                map.serialize_entry("t", t)?;
                map.end()
            }
            Self::Stream(t) => {
                let mut map = serializer.serialize_map(Some(2))?;
                map.serialize_entry("k", "stream")?;
                map.serialize_entry("t", t)?;
                map.end()
            }
            Self::BuiltIn(n) => match built_in(n) {
                Some(_t) => n.serialize(serializer),
                _ => Err(S::Error::custom(format!("unrecognized built-in type {n}",))),
            },
        }
    }
}

#[cfg(feature = "sqlx")]
impl sqlx::Type<Postgres> for Type {
    fn type_info() -> <Postgres as Database>::TypeInfo {
        sqlx::types::JsonValue::type_info()
    }
}

#[cfg(feature = "sqlx")]
impl<'q> Encode<'q, Postgres> for Type {
    fn encode_by_ref(&self, buf: &mut <Postgres as HasArguments<'q>>::ArgumentBuffer) -> IsNull {
        serde_json::to_value(self)
            .expect("type is valid json")
            .encode_by_ref(buf)
    }
}

#[cfg(feature = "sqlx")]
impl<'r> Decode<'r, Postgres> for Type {
    fn decode(
        value: <Postgres as HasValueRef<'r>>::ValueRef,
    ) -> Result<Self, sqlx::error::BoxDynError> {
        Ok(serde_json::from_value(sqlx::types::JsonValue::decode(
            value,
        )?)?)
    }
}

#[cfg(feature = "sqlx")]
impl PgHasArrayType for Type {
    fn array_type_info() -> sqlx::postgres::PgTypeInfo {
        sqlx::types::JsonValue::array_type_info()
    }
}

#[cfg(feature = "graphql")]
async_graphql::scalar!(Type);
