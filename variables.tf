variable "db_host" {
  type = string
  default= "first"
}

variable "db_name" {
  type = string
  default= "first"
}

variable "db_user" {
  default = "adminuser"
}
variable "db_password" {
  default = "Abhishek8915"
}



variable "vpc_id" {
  type = string
  default= "vpc-06c1c352d16a03fe2"
}

variable "subnet_ids" {
  type = string
  default= "subnet-029a8beb2b79e585"
}