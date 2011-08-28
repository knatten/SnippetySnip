void foo() {}

/* snippetysnip_begin:bar */
void bar() {
    foo();
}
// snippetysnip_end

// snippetysnip_begin:error
int main() {
    foo();
    return 0;
}
