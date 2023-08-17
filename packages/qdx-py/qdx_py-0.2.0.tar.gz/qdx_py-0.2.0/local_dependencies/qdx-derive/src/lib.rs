use proc_macro::TokenStream;
use quote::quote;
use syn::{Data, DeriveInput, Fields, Type};

#[proc_macro_derive(Typedef)]
pub fn typedef_derive(input: TokenStream) -> TokenStream {
    let ast: DeriveInput = syn::parse(input).unwrap();
    let name = &ast.ident;
    let name_as_str = format!("{name}");

    let description = match &ast.data {
        // Derive for a struct
        Data::Struct(data) => match &data.fields {
            Fields::Named(named) => {
                let fields = named.named.iter().map(|field| {
                    let field_name = format!("{}", field.ident.clone().unwrap());
                    let field_type = describe_type(&field.ty);
                    quote! {
                        record_fields.insert(#field_name.to_string(), #field_type)
                    }
                });
                quote!(
                    let mut record_fields = ::std::collections::BTreeMap::new();
                    #(#fields;)*
                    ::qdx_types::Type::Record(::qdx_types::Record(record_fields))
                )
            }
            Fields::Unnamed(unnamed) => {
                let fields = unnamed.unnamed.iter().map(|field| {
                    let field_type = describe_type(&field.ty);
                    quote! {
                        #field_type
                    }
                });
                quote!(::qdx_types::Type::Tuple(::qdx_types::Tuple([#(#fields,)*].into_iter().collect())))
            }
            Fields::Unit => panic!("Typedef cannot be derived for unit structs"),
        },
        // Derive for an enum
        Data::Enum(data) => {
            let variants = data.variants.iter().map(|variant| {
                let variant_name = format!("{}", variant.ident.clone());

                let variant_fields = match &variant.fields {
                    Fields::Unnamed(unnamed) => {
                        let fields = unnamed.unnamed.iter().map(|field| {
                            let field_type = describe_type(&field.ty);
                            quote! {
                                #field_type
                            }
                        });
                        Some(
                            quote! {
                                ::qdx_types::Fields::Unnamed([#(#fields,)*].into_iter().collect())
                            }
                        )
                    }
                    Fields::Named(named) => {
                        let fields = named.named.iter().map(|field| {
                            let field_name = format!("{}", field.ident.clone().unwrap());
                            let field_type = describe_type(&field.ty);
                            quote! {
                                named_fields.insert(#field_name.to_string(), #field_type)
                            }
                        });
                        Some(quote! {{
                                let mut named_fields = ::std::collections::BTreeMap::new();
                                #(#fields;)*
                                ::qdx_types::Fields::Named(named_fields)
                        }})
                    }
                    Fields::Unit => None,
                };

                match variant_fields {
                    None => {
                        quote! {
                            ::qdx_types::Variant::Tagged(#variant_name.to_string())
                        }
                    }
                    Some(variant_fields) => {
                        quote! {
                            ::qdx_types::Variant::TaggedFields(#variant_name.to_string(), #variant_fields)
                        }
                    }
                }
            });

            quote!(::qdx_types::Type::Enum(::qdx_types::Enum([#(#variants,)*].into_iter().collect())))
        }
        _ => panic!("Typedef can only be derived for structs and enums"),
    };

    let generics = ast.generics;
    let (impl_generics, ty_generics, where_clause) = generics.split_for_impl();

    let expanded = quote! {
        impl  #impl_generics ::qdx_types::Typedef for #name #ty_generics #where_clause {
            fn describe() -> ::qdx_types::Type {
                let t = { #description };
                if let Some(built_in) = ::qdx_types::built_in(#name_as_str) {
                    if t == built_in {
                        return ::qdx_types::Type::BuiltIn(#name_as_str.to_string());
                    }
                }
                t
            }
        }
    };

    TokenStream::from(expanded)
}

fn describe_type(ty: &Type) -> proc_macro2::TokenStream {
    match ty {
        Type::Path(type_path) if type_path.qself.is_none() => {
            let ident = &type_path.path.segments.last().unwrap().ident;
            let inner_types = &type_path.path.segments.last().unwrap().arguments;
            quote!(<#ident #inner_types as ::qdx_types::Typedef>::describe())
        }
        Type::Tuple(tuple) => {
            let inner_types = tuple.elems.iter().map(describe_type);
            quote!(::qdx_types::Type::Tuple(::qdx_types::Tuple([#(#inner_types,)*].into_iter().collect())))
        }
        _ => panic!("Unsupported type"),
    }
}
