# extract from:
# * https://github.com/WebAssembly/design/blob/master/BinaryEncoding.md
# * https://webassembly.github.io/spec/core/binary/instructions.html
# * https://github.com/athre0z/wasm/blob/master/wasm/opcodes.py

from wasm_tob.immtypes import *

_groups = {0x00: 'Control',
           0x1A: 'Parametric',
           0x20: 'Variable',
           0x28: 'Memory',
           0x41: 'Constant',
           0x45: 'Logical_i32',
           0x50: 'Logical_i64',
           0x5b: 'Logical_f32',
           0x61: 'Logical_f64',
           0x67: 'Arithmetic_i32',
           0x71: 'Bitwise_i32',
           0x79: 'Arithmetic_i64',
           0x83: 'Bitwise_i64',
           0x8b: 'Arithmetic_f32',
           0x99: 'Arithmetic_f64',
           0xa7: 'Conversion'}

_table = {
    # opcode:(mnemonic/name, imm_struct, pops, pushes, description)
    0x00: ('unreachable', None, 0, 0, 'trap immediately'),
    0x01: ('nop', None, 0, 0, 'no operation'),
    0x02: ('block', BlockImm(), 0, 0, 'begin a sequence of expressions'),
    0x03: ('loop', BlockImm(), 0, 0, 'begin a block which can also form control flow loops'),
    0x04: ('if', BlockImm(), 1, 0, 'begin if expression'),
    0x05: ('else', None, 0, 0, 'begin else expression of if'),
    0x0b: ('end', None, 0, 0, 'end a block, loop, or if'),
    0x0c: ('br', BranchImm(), 0, 0, 'break that targets an outer nested block'),
    0x0d: ('br_if', BranchImm(), 1, 0, 'conditional break that targets an outer nested block'),
    0x0e: ('br_table', BranchTableImm(), 1, 0, 'branch table control flow construct'),
    0x0f: ('return', None, 1, 0, 'return zero or one value from this function'),
    0x10: ('call', CallImm(), 0, 0, 'call a function by its index'),#TODO:the actual pops and pushes would be determined dynamically by the signature of the function called
    0x11: ('call_indirect', CallIndirectImm(), 1, 0, 'call a function indirect with an expected signature'),

    0x1a: ('drop', None, 1, 0, 'ignore value'),
    0x1b: ('select', None, 3, 1, 'select one of two values based on condition'),

    0x20: ('get_local', LocalVarXsImm(), 0, 1, 'read a local variable or parameter'),
    0x21: ('set_local', LocalVarXsImm(), 1, 0, 'write a local variable or parameter'),
    0x22: ('tee_local', LocalVarXsImm(), 1, 1, 'write a local variable or parameter and read the same value'),
    0x23: ('get_global', GlobalVarXsImm(), 0, 1, 'read a global variable'),
    0x24: ('set_global', GlobalVarXsImm(), 1, 0, 'write a global variable'),

    0x28: ('i32.load', MemoryImm(), 1, 1, 'load from memory'),
    0x29: ('i64.load', MemoryImm(), 1, 1, 'load from memory'),
    0x2a: ('f32.load', MemoryImm(), 1, 1, 'load from memory'),
    0x2b: ('f64.load', MemoryImm(), 1, 1, 'load from memory'),
    0x2c: ('i32.load8_s', MemoryImm(), 1, 1, 'load from memory'),
    0x2d: ('i32.load8_u', MemoryImm(), 1, 1, 'load from memory'),
    0x2e: ('i32.load16_s', MemoryImm(), 1, 1, 'load from memory'),
    0x2f: ('i32.load16_u', MemoryImm(), 1, 1, 'load from memory'),
    0x30: ('i64.load8_s', MemoryImm(), 1, 1, 'load from memory'),
    0x31: ('i64.load8_u', MemoryImm(), 1, 1, 'load from memory'),
    0x32: ('i64.load16_s', MemoryImm(), 1, 1, 'load from memory'),
    0x33: ('i64.load16_u', MemoryImm(), 1, 1, 'load from memory'),
    0x34: ('i64.load32_s', MemoryImm(), 1, 1, 'load from memory'),
    0x35: ('i64.load32_u', MemoryImm(), 1, 1, 'load from memory'),
    0x36: ('i32.store', MemoryImm(), 2, 0, 'store to memory'),
    0x37: ('i64.store', MemoryImm(), 2, 0, 'store to memory'),
    0x38: ('f32.store', MemoryImm(), 2, 0, 'store to memory'),
    0x39: ('f64.store', MemoryImm(), 2, 0, 'store to memory'),
    0x3a: ('i32.store8', MemoryImm(), 2, 0, 'store to memory'),
    0x3b: ('i32.store16', MemoryImm(), 2, 0, 'store to memory'),
    0x3c: ('i64.store8', MemoryImm(), 2, 0, 'store to memory'),
    0x3d: ('i64.store16', MemoryImm(), 2, 0, 'store to memory'),
    0x3e: ('i64.store32', MemoryImm(), 2, 0, 'store to memory'),
    0x3f: ('current_memory', CurGrowMemImm(), 0, 1, 'query the size of memory'),
    0x40: ('grow_memory', CurGrowMemImm(), 0, 0, 'grow the size of memory'),

    0x41: ('i32.const', I32ConstImm(), 0, 1, 'a constant value interpreted as i32'),
    0x42: ('i64.const', I64ConstImm(), 0, 1, 'a constant value interpreted as i64'),
    0x43: ('f32.const', F32ConstImm(), 0, 1, 'a constant value interpreted as f32'),
    0x44: ('f64.const', F64ConstImm(), 0, 1, 'a constant value interpreted as f64'),

    0x45: ('i32.eqz', None, 1, 1, 'compare equal to zero (return 1 if operand is zero, 0 otherwise)'),
    0x46: ('i32.eq', None, 2, 1, 'sign-agnostic compare equal'),
    0x47: ('i32.ne', None, 2, 1, 'sign-agnostic compare unequal'),
    0x48: ('i32.lt_s', None, 2, 1, 'signed less than'),
    0x49: ('i32.lt_u', None, 2, 1, 'unsigned less than'),
    0x4a: ('i32.gt_s', None, 2, 1, 'signed greater than'),
    0x4b: ('i32.gt_u', None, 2, 1, 'unsigned greater than'),
    0x4c: ('i32.le_s', None, 2, 1, 'signed less than or equal'),
    0x4d: ('i32.le_u', None, 2, 1, 'unsigned less than or equal'),
    0x4e: ('i32.ge_s', None, 2, 1, 'signed greater than or equal'),
    0x4f: ('i32.ge_u', None, 2, 1, 'unsigned greater than or equal'),

    0x50: ('i64.eqz', None, 1, 1, 'compare equal to zero (return 1 if operand is zero, 0 otherwise)'),
    0x51: ('i64.eq', None, 2, 1, 'sign-agnostic compare equal'),
    0x52: ('i64.ne', None, 2, 1, 'sign-agnostic compare unequal'),
    0x53: ('i64.lt_s', None, 2, 1, 'signed less than'),
    0x54: ('i64.lt_u', None, 2, 1, 'unsigned less than'),
    0x55: ('i64.gt_s', None, 2, 1, 'signed greater than'),
    0x56: ('i64.gt_u', None, 2, 1, 'unsigned greater than'),
    0x57: ('i64.le_s', None, 2, 1, 'signed less than or equal'),
    0x58: ('i64.le_u', None, 2, 1, 'unsigned less than or equal'),
    0x59: ('i64.ge_s', None, 2, 1, 'signed greater than or equal'),
    0x5a: ('i64.ge_u', None, 2, 1, 'unsigned greater than or equal'),

    0x5b: ('f32.eq', None, 2, 1, 'compare ordered and equal'),
    0x5c: ('f32.ne', None, 2, 1, 'compare unordered or unequal'),
    0x5d: ('f32.lt', None, 2, 1, 'compare ordered and less than'),
    0x5e: ('f32.gt', None, 2, 1, 'compare ordered and less than or equal'),
    0x5f: ('f32.le', None, 2, 1, 'compare ordered and greater than'),
    0x60: ('f32.ge', None, 2, 1, 'compare ordered and greater than or equal'),

    0x61: ('f64.eq', None, 2, 1, 'compare ordered and equal'),
    0x62: ('f64.ne', None, 2, 1, 'compare unordered or unequal'),
    0x63: ('f64.lt', None, 2, 1, 'compare ordered and less than'),
    0x64: ('f64.gt', None, 2, 1, 'compare ordered and less than or equal'),
    0x65: ('f64.le', None, 2, 1, 'compare ordered and greater than'),
    0x66: ('f64.ge', None, 2, 1, 'compare ordered and greater than or equal'),

    0x67: ('i32.clz', None, 1, 1, 'sign-agnostic count leading zero bits (All zero bits are considered leading if the value is zero)'),
    0x68: ('i32.ctz', None, 1, 1, 'sign-agnostic count trailing zero bits (All zero bits are considered trailing if the value is zero)'),
    0x69: ('i32.popcnt', None, 1, 1, 'sign-agnostic count number of one bits'),
    0x6a: ('i32.add', None, 2, 1, 'sign-agnostic addition'),
    0x6b: ('i32.sub', None, 2, 1, 'sign-agnostic subtraction'),
    0x6c: ('i32.mul', None, 2, 1, 'sign-agnostic multiplication (lower 32-bits)'),
    0x6d: ('i32.div_s', None, 2, 1, 'signed division (result is truncated toward zero)'),
    0x6e: ('i32.div_u', None, 2, 1, 'unsigned division (result is floored)'),
    0x6f: ('i32.rem_s', None, 2, 1, 'signed remainder (result has the sign of the dividend)'),
    0x70: ('i32.rem_u', None, 2, 1, 'unsigned remainder'),

    0x71: ('i32.and', None, 2, 1, 'sign-agnostic bitwise and'),
    0x72: ('i32.or', None, 2, 1, 'sign-agnostic bitwise inclusive or'),
    0x73: ('i32.xor', None, 2, 1, 'sign-agnostic bitwise exclusive or'),
    0x74: ('i32.shl', None, 2, 1, 'sign-agnostic shift left'),
    0x75: ('i32.shr_s', None, 2, 1, 'sign-replicating (arithmetic) shift right'),
    0x76: ('i32.shr_u', None, 2, 1, 'zero-replicating (logical) shift right'),
    0x77: ('i32.rotl', None, 2, 1, 'sign-agnostic rotate left'),
    0x78: ('i32.rotr', None, 2, 1, 'sign-agnostic rotate right'),

    0x79: ('i64.clz', None, 1, 1, 'sign-agnostic count leading zero bits (All zero bits are considered leading if the value is zero)'),
    0x7a: ('i64.ctz', None, 1, 1, 'sign-agnostic count trailing zero bits (All zero bits are considered trailing if the value is zero)'),
    0x7b: ('i64.popcnt', None, 1, 1, 'sign-agnostic count number of one bits'),
    0x7c: ('i64.add', None, 2, 1, 'sign-agnostic addition'),
    0x7d: ('i64.sub', None, 2, 1, 'sign-agnostic subtraction'),
    0x7e: ('i64.mul', None, 2, 1, 'sign-agnostic multiplication (lower 32-bits)'),
    0x7f: ('i64.div_s', None, 2, 1, 'signed division (result is truncated toward zero)'),
    0x80: ('i64.div_u', None, 2, 1, 'unsigned division (result is floored)'),
    0x81: ('i64.rem_s', None, 2, 1, 'signed remainder (result has the sign of the dividend)'),
    0x82: ('i64.rem_u', None, 2, 1, 'unsigned remainder'),

    0x83: ('i64.and', None, 2, 1, 'sign-agnostic bitwise and'),
    0x84: ('i64.or', None, 2, 1, 'sign-agnostic bitwise inclusive or'),
    0x85: ('i64.xor', None, 2, 1, 'sign-agnostic bitwise exclusive or'),
    0x86: ('i64.shl', None, 2, 1, 'sign-agnostic shift left'),
    0x87: ('i64.shr_s', None, 2, 1, 'sign-replicating (arithmetic) shift right'),
    0x88: ('i64.shr_u', None, 2, 1, 'zero-replicating (logical) shift right'),
    0x89: ('i64.rotl', None, 2, 1, 'sign-agnostic rotate left'),
    0x8a: ('i64.rotr', None, 2, 1, 'sign-agnostic rotate right'),

    0x8b: ('f32.abs', None, 1, 1, 'absolute value'),
    0x8c: ('f32.neg', None, 1, 1, 'negation'),
    0x8d: ('f32.ceil', None, 2, 1, 'ceiling operator'),
    0x8e: ('f32.floor', None, 2, 1, 'floor operator'),
    0x8f: ('f32.trunc', None, 2, 1, 'round to nearest integer towards zero'),
    0x90: ('f32.nearest', None, 2, 1, 'round to nearest integer, ties to even'),
    0x91: ('f32.sqrt', None, 2, 1, 'square root'),
    0x92: ('f32.add', None, 2, 1, 'addition'),
    0x93: ('f32.sub', None, 2, 1, 'subtraction'),
    0x94: ('f32.mul', None, 2, 1, 'multiplication'),
    0x95: ('f32.div', None, 2, 1, 'division'),
    0x96: ('f32.min', None, 2, 1, 'minimum (binary operator); if either operand is NaN, returns NaN'),
    0x97: ('f32.max', None, 2, 1, 'maximum (binary operator); if either operand is NaN, returns NaN'),
    0x98: ('f32.copysign', None, 2, 1, 'copysign'),

    0x99: ('f64.abs', None, 1, 1, 'absolute value'),
    0x9a: ('f64.neg', None, 1, 1, 'negation'),
    0x9b: ('f64.ceil', None, 2, 1, 'ceiling operator'),
    0x9c: ('f64.floor', None, 2, 1, 'floor operator'),
    0x9d: ('f64.trunc', None, 2, 1, 'round to nearest integer towards zero'),
    0x9e: ('f64.nearest', None, 2, 1, 'round to nearest integer, ties to even'),
    0x9f: ('f64.sqrt', None, 2, 1, 'square root'),
    0xa0: ('f64.add', None, 2, 1, 'addition'),
    0xa1: ('f64.sub', None, 2, 1, 'subtraction'),
    0xa2: ('f64.mul', None, 2, 1, 'multiplication'),
    0xa3: ('f64.div', None, 2, 1, 'division'),
    0xa4: ('f64.min', None, 2, 1, 'minimum (binary operator); if either operand is NaN, returns NaN'),
    0xa5: ('f64.max', None, 2, 1, 'maximum (binary operator); if either operand is NaN, returns NaN'),
    0xa6: ('f64.copysign', None, 2, 1, 'copysign'),

    0xa7: ('i32.wrap/i64', None, 1, 1, 'wrap a 64-bit integer to a 32-bit integer'),
    0xa8: ('i32.trunc_s/f32', None, 1, 1, 'truncate a 32-bit float to a signed 32-bit integer'),
    0xa9: ('i32.trunc_u/f32', None, 1, 1, 'truncate a 32-bit float to an unsigned 32-bit integer'),
    0xaa: ('i32.trunc_s/f64', None, 1, 1, 'truncate a 64-bit float to a signed 32-bit integer'),
    0xab: ('i32.trunc_u/f64', None, 1, 1, 'truncate a 64-bit float to an unsigned 32-bit integer'),
    0xac: ('i64.extend_s/i32', None, 1, 1, 'extend a signed 32-bit integer to a 64-bit integer'),
    0xad: ('i64.extend_u/i32', None, 1, 1, 'extend an unsigned 32-bit integer to a 64-bit integer'),
    0xae: ('i64.trunc_s/f32', None, 1, 1, 'truncate a 32-bit float to a signed 64-bit integer'),
    0xaf: ('i64.trunc_u/f32', None, 1, 1, 'truncate a 32-bit float to an unsigned 64-bit integer'),
    0xb0: ('i64.trunc_s/f64', None, 1, 1, 'truncate a 64-bit float to a signed 64-bit integer'),
    0xb1: ('i64.trunc_u/f64', None, 1, 1, 'truncate a 64-bit float to an unsigned 64-bit integer'),
    0xb2: ('f32.convert_s/i32', None, 1, 1, 'convert a signed 32-bit integer to a 32-bit float'),
    0xb3: ('f32.convert_u/i32', None, 1, 1, 'convert an unsigned 32-bit integer to a 32-bit float'),
    0xb4: ('f32.convert_s/i64', None, 1, 1, 'convert a signed 64-bit integer to a 32-bit float'),
    0xb5: ('f32.convert_u/i64', None, 1, 1, 'convert an unsigned 64-bit integer to a 32-bit float'),
    0xb6: ('f32.demote/f64', None, 1, 1, 'demote a 64-bit float to a 32-bit float'),
    0xb7: ('f64.convert_s/i32', None, 1, 1, 'convert a signed 32-bit integer to a 64-bit float'),
    0xb8: ('f64.convert_u/i32', None, 1, 1, 'convert an unsigned 32-bit integer to a 64-bit float'),
    0xb9: ('f64.convert_s/i64', None, 1, 1, 'convert a signed 64-bit integer to a 64-bit float'),
    0xba: ('f64.convert_u/i64', None, 1, 1, 'convert an unsigned 64-bit integer to a 64-bit float'),
    0xbb: ('f64.promote/f32', None, 1, 1, 'promote a 32-bit float to a 64-bit float'),
    0xbc: ('i32.reinterpret/f32', None, 1, 1, 'reinterpret the bits of a 32-bit float as a 32-bit integer'),
    0xbd: ('i64.reinterpret/f64', None, 1, 1, 'reinterpret the bits of a 64-bit float as a 64-bit integer'),
    0xbe: ('f32.reinterpret/i32', None, 1, 1, 'reinterpret the bits of a 32-bit integer as a 32-bit float'),
    0xbf: ('f64.reinterpret/i64', None, 1, 1, 'reinterpret the bits of a 64-bit integer as a 64-bit float'),
}


class Wasm(object):
    """Wasm bytecode."""

    def __init__(self):
        self.table = _table
        self.reverse_table = self._get_reverse_table()

    def _get_reverse_table(self):
        """Build an internal table used in the assembler."""
        # opcode:(mnemonic/name, imm_struct, pops, pushes, description)
        reverse_table = {}
        for (opcode, (mnemonic, imm_struct,
                      pops, pushes, description)) in self.table.items():
            reverse_table[mnemonic] = opcode, mnemonic, imm_struct, pops, pushes, description
        return reverse_table
