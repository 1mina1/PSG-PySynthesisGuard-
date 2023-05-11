/***************************************************************************************************************/
/*
 Author: Omar Ayman Abdel-Motaal

 Design Name:  ATM.FSM
 Module Name:  u_atm_fsm.v 
 Project Name: ATM
 Describtion:  This Module aim to implement FSM of ATM
/****************************************************************************************************************/
module u_atm_fsm
    #(parameter CNS = 64, CIS = 4,DBD=16 ,Pass_width=16,balance_width=14 )
	(
    input wire	                        clk,
	input wire                          rst,
	input wire                          ic,//insert card
	input wire                          mt,//more transaction
    input wire     [CNS-1:0]            credit_number, destination_number, 
	input wire     [Pass_width-1:0]     en_password, new_password,
	input wire     [15:0]               en_ammount_money,
    input wire     [2:0]                option,
	input wire     [3:0]                keyboard,
	input 								enter,


	output reg                          card_accepted,
	output reg                          account_balance,
	output reg 						    Insuffucient_flag,
	output reg                          y0,y1,y2,y3,y4,y5,y6,y7,y11,y10,y8,y12
	);


	

reg [balance_width-1:0]  source_server_balance_reg ;
reg [Pass_width-1:0]     source_server_pass_reg ;
reg [balance_width-1:0]  destination_server_balance_reg ;
reg [Pass_width-1:0]     destination_server_pass_reg ;





wire                          source_exists;
wire                          destination_exists;
wire     [balance_width-1:0]  source_server_balance;
wire     [balance_width-1:0]  destination_server_balance;
wire     [Pass_width-1:0]     source_server_pass;
wire     [Pass_width-1:0]     destination_server_pass;
wire     [CIS-1:0]            SINDEX;
wire     [CIS-1:0]            DINDEX;
u_card_scan check_source_account_exist(.credit_number(credit_number),.card_pass(source_server_pass),.card_index(SINDEX), .card_balance(source_server_balance),.card_found_flag(source_exists) );
u_card_scan check_destination_account_exist(.credit_number(destination_number),.card_pass(destination_server_pass),.card_index(DINDEX) ,.card_balance(destination_server_balance),.card_found_flag(destination_exists) );
 
 /***************************** Intial Blocks ****************************/
 reg [2:0] wrong_tries;
 initial begin
 wrong_tries =0;
 end
 
 /********************************* assign ******************************/
 wire [2:0]   trials;
 wire [12:0]  deposit_max_val;
 assign trials='d5;
 assign deposit_max_val='d5000;
/********************************* States *******************************/	
localparam [3:0]      idle=4'b0000,             //s0
                      blance_check=4'b0001,     //s1
					  withdraw=4'b0010,         //s2
					  deposit=4'b0011,          //s3
					  transfer=4'b0100, 		//s4
					  exit=4'b0101,             //s5
					  new_pass=4'b0110,         //s6
					  lang_used=4'b0111,        //s7
					  scan_card=4'b1000,         //s8
					  enter_pass=4'b1001,       //s9
					  option_select=4'b1010,    //s10 
					  anything_else=4'b1011;    //s11
                     
					  
/*****************************************************************************/	
reg [3:0] current_state, next_state;

/**************************** States Transition *****************************/	
always @(posedge clk or negedge rst)
begin
	if(!rst)
	begin
		current_state<= idle;
		
		end
	else
		current_state<=next_state;
end				  

/*****************************************************************************/
/*******************************  Timer **************************************/
reg [5:0] counter;
always @(posedge clk or negedge rst)
begin
	if(!rst)
	begin
		counter<= 0;	
	end
	else
	if(current_state==next_state)
	counter<=counter+1'd1;
	else
		counter<=0;
end	     

    
/*****************************************************************************/
always @(*)
begin
case(current_state)
		idle:begin	
							if(ic)//insert  card
									begin
										next_state =  scan_card;	
										end									

							else
								begin
								next_state =  idle;							
								end
					  end

	scan_card:begin
				if(counter <5 )begin				
									if(source_exists==1)//card scan
										begin											
											source_server_balance_reg = source_server_balance;
											source_server_pass_reg = source_server_pass;							 
											card_accepted =1;	
											wrong_tries='d0;											
											next_state = lang_used;
										end
									else
										begin
																														
																	source_server_balance_reg = 0;
																	source_server_pass_reg = 0;							 
																	card_accepted =0;
																	wrong_tries='d0;
																	next_state =  scan_card;	
																														
										end							
								end
								  else begin
								next_state = idle;		
					  end
	
	



end	
					  
					  
					  
					  
	lang_used:   begin		          
					  if(counter <5 )begin
							   if(keyboard != 0)				  
								next_state = enter_pass;
								else
								 next_state = lang_used;
					  end else
						next_state = idle;
							
				 end			  
		enter_pass: begin
		    if(counter <5 )begin
					if(enter) begin
													if(en_password == source_server_pass_reg)
														begin
															next_state = option_select;
															wrong_tries='d0;
														end
													else
														begin
															if ((wrong_tries != trials) )
																begin
																	wrong_tries=wrong_tries+1'd1;
																	next_state = enter_pass;
																end
															else 
															  begin
																wrong_tries='d0;							
																next_state = idle;
															  end
														end	
								end
			else begin
				next_state=enter_pass;end
							end 
							  else
								next_state = idle;
											
					  end
		option_select:begin
								if(option==0)
								begin
									if(counter<5) begin
									next_state = option_select;
									end else 
									next_state = idle;
									
								end else
								begin
											  
										if(option == 'b10)
											begin
											next_state = withdraw;
									
											end
										else if(option == 'b01)
											begin
											next_state = blance_check;
											
											end
										else if(option == 'b11)
											begin
											next_state = deposit;
										
											end
										else if(option == 'b100)
											begin
											next_state = transfer;
											
											end
										else if(option == 'b110)
											begin
											next_state = new_pass;
											
											end	
										else if(option == 'b101)
											begin
											next_state = exit;
											
											end
										else //comment : if option selected wrong remain at Menu panel.
											begin
											next_state = option_select;
											
											end
								end

						  end
		withdraw: begin
				    /*******************************/
				        Insuffucient_flag=0;
				    /*******************************/
		    if(counter <10 )begin
						if(enter) begin
											if((en_ammount_money <= source_server_balance_reg)&&(en_ammount_money!=0)) //check ammount entered is less that blance in account
												begin
													 source_server_balance_reg=source_server_balance_reg-en_ammount_money;
													 account_balance=source_server_balance_reg;

													next_state = anything_else;
													end
											else
												begin
													if(en_ammount_money==0) 
													begin

														  next_state = withdraw;
													end
													else 
														begin													
														next_state = option_select;
														/*******************************/
														     Insuffucient_flag=1;
														/*******************************/
														end
												end
									end
							else begin
							next_state=withdraw;
								end
							end
					        else begin
					        next_state = idle;
							end		
		
					 end
		blance_check:begin
							 if(counter>5)
								  begin
									 next_state = anything_else;
								  end
							 else begin
								next_state = blance_check;
							 end
												
					 end

		deposit: begin
		         if(counter <10 )begin		
						if(enter) begin				 
											if((en_ammount_money <= deposit_max_val)&& (en_ammount_money!=0)) 
													begin
														 source_server_balance_reg=source_server_balance_reg+en_ammount_money;
														 account_balance=source_server_balance_reg;
														next_state = anything_else;
														end
												else
													begin
														if(en_ammount_money==0)
														begin										
															   next_state = deposit;
														end
														else begin
														next_state = option_select;
														end
													end
							     end
								else begin
									next_state=deposit;
									end
								end
					             else
					             next_state = idle;		
		
			   end 
						 
						 
						 

		anything_else: begin
		 if(counter <5 )begin
								if(mt)//More transaction
									begin
									next_state = option_select;
									end
								else
									begin
									next_state =  anything_else;
									end
				end
								else
									begin
									next_state =  exit;
									end
							end
		exit:begin				
                     next_state =  idle;					
					  end
	/*********************************************************************/				  
		new_pass:begin		
                if(counter<10)begin
					if (enter)begin
							source_server_pass_reg = new_password;
							next_state = anything_else;	
							end
                   else	begin	
                     next_state = new_pass;					
					  end	
				end
				   else begin
				    next_state=idle;end
				end
	/*********************************************************************/					  
		transfer:begin			
if(counter<5)		
begin
			if(enter)begin
					if(destination_exists)//Destination card number exist
							   begin
									destination_server_balance_reg = destination_server_balance;
									destination_server_pass_reg = destination_server_pass;		
										   if((en_ammount_money <= source_server_balance_reg)&&(en_ammount_money!=0))
										   begin
													source_server_balance_reg = source_server_balance_reg - en_ammount_money;
													destination_server_balance_reg = destination_server_balance_reg + en_ammount_money;
													account_balance=source_server_balance_reg;
												next_state = anything_else;
											end
											else
											begin
												if(en_ammount_money==0) 
												begin																				
														  next_state = transfer;
												end 
												else
												begin											
													next_state = option_select;
												end
											end
							   end 
							   else begin
								destination_server_balance_reg = 0;
								destination_server_pass_reg = 0;	
								next_state = transfer; 
							   end
						end
							else begin
							next_state=transfer;
								end
						  end
							else
							next_state = idle;						  
				 end					  
endcase
end

always @(*)
 begin

		
		y0=0;
		y1=0;
		y5=0;
		y11=0;
		y10=0;
		y7=0;
		y3=0;
		y2=0;
		y4=0;
		y6=0;
		y8=0;

  case(current_state)
  	idle     : begin
				y0=1;
            end
  	blance_check     : begin
				y1=1;
            end

	exit     : begin
                y5=1;
            end	
	anything_else     : begin
				y11=1;
            end	
	option_select     : begin
				y10=1;
            end	

	lang_used     : begin
				y7=1;
            end	
	scan_card :begin
	y8=1;
	end
	
	new_pass :begin
				y12=1;
			  end			
	deposit     : begin
				y3=1;
            end
	withdraw    : begin
				y2=1;				
            end
	transfer    : begin

				y4=1;				
            end
	enter_pass    : begin

				y6=1;
            end


 endcase
end
endmodule