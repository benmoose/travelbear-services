package web

import "testing"

func TestHello(t *testing.T) {
	want := "Hello world"
	if got := Hello(); got != want {
		t.Errorf("Hello() = %q, but expected %q", got, want)
	}
}
