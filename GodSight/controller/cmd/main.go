package main

import (
    "controller/pkg/config"
    "controller/pkg/handler"
    "controller/pkg/middleware"
    "github.com/gorilla/mux"
    "log"
    "net/http"
)

func main() {
    r := mux.NewRouter()

    // Middleware
    r.Use(middleware.Logger)

    // Routes
    r.HandleFunc("/api/users", handler.CreateUser).Methods("POST")
    r.HandleFunc("/api/users/{id}", handler.GetUser).Methods("GET")
    r.HandleFunc("/api/login", handler.Authenticate).Methods("POST")

    // Apply the JWT middleware to secure routes
    r.HandleFunc("/api/secure", middleware.JwtAuthentication(handler.SecureEndpoint)).Methods("GET")

    http.Handle("/", r)
    log.Fatal(http.ListenAndServe(":"+config.Port, r))
}
