# https://klotzandrew.com/blog/deploy-an-ec2-to-run-docker-with-terraform

resource "aws_ecr_repository" "my_first_ecr_repo" {
  name = "uptime-kuma-ecr_repo"
  image_tag_mutability = "MUTABLE"

  tags = {
    project = "uptime-kuma-jag-isb"
  }
}

# VPC / Networking

data "aws_vpc" "default" {
  id = var.vpc_id
}

data "aws_subnet" "default_subnet" {
  id = var.subnet_id
}

resource "aws_network_interface" "foo" {
  subnet_id   = data.aws_subnet.default_subnet.id
  security_groups = [module.dev_ssh_sg.security_group_id, module.ec2_sg.security_group_id]

  tags = {
    Name = "primary_network_interface"
    project = "uptime-kuma-jag-isb"
  }
}

  
# EC2 
resource "aws_iam_role" "ec2_role_uptime_kuma" {
  name = "ec2_role_uptime_kuma"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF

  tags = {
    project = "uptime-kuma-jag-isb"
  }
}

resource "aws_iam_instance_profile" "ec2_profile_uptime_kuma" {
  name = "EC2-Role-Uptime-Kuma"
  role = aws_iam_role.ec2_role_uptime_kuma.name
}

resource "aws_iam_role_policy" "ec2_policy" {
  name = "ec2_policy"
  role = aws_iam_role.ec2_role_uptime_kuma.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

module "dev_ssh_sg" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "ssh_ec2_sg"
  description = "Security group for ec2_sg"
  vpc_id      = data.aws_vpc.default.id

  ingress_cidr_blocks = ["127.0.0.1/32"]
  ingress_rules       = ["ssh-tcp"]
}

module "ec2_sg" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "http_ec2_sg"
  description = "Security group for ec2_sg"
  vpc_id      = data.aws_vpc.default.id

  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules       = ["https-443-tcp", "all-icmp"]
  egress_rules        = ["all-all"]
}


resource "aws_instance" "web" {
  ami = "ami-095819c19b51bc983"
  instance_type = "t2.micro"
  
  # root disk
  root_block_device {
    volume_size           = "20"
    volume_type           = "gp2"
    encrypted             = true
    delete_on_termination = true
  }
  # data disk
  ebs_block_device {
    device_name           = "/dev/xvda"
    volume_size           = "50"
    volume_type           = "gp2"
    encrypted             = true
    delete_on_termination = true
  }

  vpc_security_group_ids = [
    module.ec2_sg.security_group_id,
    module.dev_ssh_sg.security_group_id
  ]

  subnet_id = data.aws_subnet.default_subnet.id
  iam_instance_profile = "EC2-Role-Uptime-Kuma"

  tags = {
    project = "uptime-kuma-jag-isb"
  }

  key_name = "cameron-wilson-key-pair"

}

# resource "aws_ebs_encryption_by_default" "enabled" {
#      enabled = true
# }

