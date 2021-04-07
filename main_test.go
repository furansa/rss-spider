package main

import (
	"testing"
)

func TestDummy(t *testing.T) {
	expected := "Dummy output"
	got := expected

	if got != expected {
		t.Errorf("Did not get expected result %q, got: %q\n", expected, got)
	}
}
