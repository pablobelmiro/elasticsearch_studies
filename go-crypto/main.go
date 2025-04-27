package main

import (
	"encoding/json"
	"fmt"
	"net"
	"net/http"
	"time"
)

type CryptoData struct {
	Symbol string `json:"symbol"`
	Price float64 `json:"price"`
	Time string `json:"time"`
	Volume float64 `json:"volume"`
}

func fetchBitcoinData()(*CryptoData, error) {
	endpoint := "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_vol=true"

	resp, err := http.Get(endpoint)
	if err != nil {
		return nil, fmt.Errorf("request error: %v", err)
	}

	defer resp.Body.Close()

	//Decoding response
	var apiResponse map[string]map[string]float64
	if err := json.NewDecoder(resp.Body).Decode(&apiResponse); err != nil {
		return nil, fmt.Errorf("decode error: %v", err)
		
	}

	priceData, ok := apiResponse["bitcoin"]
	if !ok {
		return nil, fmt.Errorf("bitcoin data dosn't exists")
		
	}

	data := &CryptoData{
		Symbol: "bitcoin",
		Price: priceData["usd"],
		Volume: priceData["usd_24h_vol"],
		Time: time.Now().Format(time.RFC3339),
	}

	return data, nil
}

func sendToLogstash(data *CryptoData) error {
	// Connecting to logstash
	conn, err := net.Dial("tcp", "logstash:5000")
	if err != nil {
		return fmt.Errorf("logstash connection error: %v", err)
	}
	defer conn.Close()

	jsonData, err := json.Marshal(data)
	if err != nil {
		fmt.Println("Serialize error:", err)
	}

	_, err = conn.Write(append(jsonData, '\n'))
	if err != nil {
		return fmt.Errorf("erro ao enviar os dados para o Logstash: %v", err)

	}

	fmt.Println("data sended: ", string(jsonData))

	return nil
}

func bitcoinHandler(w http.ResponseWriter, r *http.Request) {
	data, err := fetchBitcoinData()
	if err != nil {
		http.Error(w, fmt.Sprintf("fetch bitcoin failed: %v", err), http.StatusInternalServerError)
		return
	}

	if err := sendToLogstash(data); err != nil {
		http.Error(w, fmt.Sprintf("Logstash connection failed: %v", err), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(data)
}

func main(){
	http.HandleFunc("/bitcoin", bitcoinHandler)

	fmt.Println("Serving on 8080...")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Println("Error to initialize server: ", err)
	}
}