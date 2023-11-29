package main

import (
	"log"
	"strings"
	"time"

	"github.com/faiface/beep/generators"
	"github.com/faiface/beep/speaker"
	"github.com/gocolly/colly/v2"
)

func main() {
	url := "https://www.bellway.co.uk/new-homes/kent/alkerden-heights/the-arkwright-4-bedroom-detached-home"
	// url := "https://www.bellway.co.uk/new-homes/kent/alkerden-heights/the-bowyer-4-bedroom-detached-home"

	c := colly.NewCollector()
	speaker.Init(44100, 4096)
	s, err := generators.SinTone(440, 5)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Starting crawler")
	ch := make(chan interface{}, 1)
	c.OnHTML("body > main > div:nth-child(1) > div > div.details.static > div.left > span:nth-child(2)", func(e *colly.HTMLElement) {
		txt := e.Text

		if !strings.Contains(txt, "£") {
			log.Println(txt)
			time.Sleep(10 * time.Second)
			c.Visit(url)
			return
		}
		log.Println(e.Text)
		speaker.Play(s)
		<-ch
	})

	c.AllowURLRevisit = true
	c.Visit(url)

}
