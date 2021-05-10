package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

func main() {
	router := mux.NewRouter()

	// Serving static files
	router.PathPrefix("/").Handler(http.FileServer(http.Dir("./static/")))

	// Prometheus endpoint
	router.Path("/metrics").Handler(promhttp.Handler())

	fmt.Println("Serving requests on port 9001")
	err := http.ListenAndServe(":9001", router)
	log.Fatal(err)
}
