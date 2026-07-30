INTENT = [
    "payment",
    "refund",
    "shipping",
    "ordering",
    "request",
    "order_tracking",
    "account",
    "technical_support",
    "product_information",
    "cancel_order",
    "returning_products",
    "other",
]

INTENT_KEYWORDS = {

    "cancel_order": [
        "cancel order",
        "cancel my order",
        "I want to cancel",
        "order cancellation",
        "stop my order",
        "remove order",
    ],

    "order_tracking": [
        "track order",
        "order status",
        "track my order",
        "order tracking",
        "status of my order",
    ],

    "technical_support": [
        "technical support",
        "not working",
        "error",
        "bug",
        "issue",
        "problem",
        "can't access",
        "help with",
        "broken",
        "glitch",
    ],

    "refund": [
        "refund",
        "money back",
        "return my money",
        "cancel payment",
        "get my money back",
        "reimburse",
    ],

    "account": [
        "account",
        "login",
        "sign in",
        "sign up",
        "register",
        "password",
        "username",
        "profile",
        "change email",
        "update account",
    ],

    "product_information": [
        "product information",
        "product details",
        "specifications",
        "what is",
        "tell me about",
        "product info",
        "features",
        "price",
        "available",
        "in stock",
    ],

    "returning_products": [
        "return",
        "returning products",
        "send back",
        "return policy",
        "how to return",
        "product return",
        "exchange",
    ],

    "payment": [
        "payment",
        "credit card",
        "mastercard",
        "visa",
        "paypal",
        "pay",
        "checkout",
    ],

    "shipping": [
        "shipping",
        "delivery",
        "package",
        "shipment",
        "deliver",
        "shipping cost",
        "where is my package"
    ],

    "request": [
        "request",
        "ask for",
        "I need",
        "can I get",
    ],

    "ordering": [
        "order",
        "buy",
        "purchase",
        "place an order",
        "add to cart",
    ],

    "other": [
        "other",
        "something else",
        "different",
        "general question",
        "help",
        "support",
    ],
}