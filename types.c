typedef unsigned char u8;
typedef unsigned long long u64;
static const u8 _9[32] = {9};
typedef long long i64;
typedef i64 field_elem[16];
static const field_elem _121665 = {0xDB41, 1};

void main(){
  int i = 0;
  for(i = 0; i < 16; i++){
    printf("%lld\n",_121665[i]);
  }
}
