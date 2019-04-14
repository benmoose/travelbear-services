package main

import (
	"fmt"
	"os"

	"Gatekeeper/web"
)

func main() {
	stack := os.Getenv("stack")
	fmt.Printf("STACK: %s\n", stack)

	fmt.Printf(web.Hello())
}
