package model

type User struct {
    ID       uint   `json:"id"`
    Username string `json:"username"`
    Password string `json:"password"` // Store hashed passwords only
    Role     string `json:"role"`
}
