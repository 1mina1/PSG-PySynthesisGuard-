module adder(
    input [3:0] in1,
    input [3:0] in2,
    output [3:0] out
);
    assign out = 1*2*3;

    always@(*) begin
        in1 = in2 +in1;
        in1 = in1+in1;
        in2 = in2*in1;
    end
endmodule