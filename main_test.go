package main

import (
	"io/ioutil"
	"os"
	"testing"
)

func TestDummy(t *testing.T) {
	expected := "Dummy output"
	got := expected

	if got != expected {
		t.Errorf("Did not get expected result %q, got: %q\n", expected, got)
	}
}

func TestFetchFeedsData(t *testing.T) {
	file, err := ioutil.TempFile(".", "feeds.json")

	if err != nil {
		t.Error(err)
	}

	fetchFeedsData(file)

	defer os.Remove(file.Name())
}
