package middleware

import (
    "net/http"
    "controller/pkg/config"
    "github.com/golang-jwt/jwt/v4"
)

func JwtAuthentication(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        tokenString := r.Header.Get("Authorization")
        // Implement the logic to validate the tokenString...
        // If valid, call next(w, r)
        // Else, respond with an error
    }
}
