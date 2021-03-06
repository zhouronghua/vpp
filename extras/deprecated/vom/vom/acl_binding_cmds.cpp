/*
 * Copyright (c) 2017 Cisco and/or its affiliates.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at:
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "vom/acl_binding_cmds.hpp"

DEFINE_VAPI_MSG_IDS_ACL_API_JSON;

namespace VOM {
namespace ACL {
namespace binding_cmds {
template <>
rc_t
l3_bind_cmd::issue(connection& con)
{
  msg_t req(con.ctx(), std::ref(*this));

  auto& payload = req.get_request().get_payload();
  payload.sw_if_index = m_itf.value();
  payload.is_add = 1;
  payload.is_input = (m_direction == direction_t::INPUT ? 1 : 0);
  payload.acl_index = m_acl.value();

  VAPI_CALL(req.execute());

  return (wait());
}

template <>
std::string
l3_bind_cmd::to_string() const
{
  std::ostringstream s;
  s << "l3-acl-bind:[" << m_direction.to_string()
    << " itf:" << m_itf.to_string() << " acl:" << m_acl.to_string() << "]";

  return (s.str());
}

template <>
rc_t
l3_unbind_cmd::issue(connection& con)
{
  msg_t req(con.ctx(), std::ref(*this));

  auto& payload = req.get_request().get_payload();
  payload.sw_if_index = m_itf.value();
  payload.is_add = 0;
  payload.is_input = (m_direction == direction_t::INPUT ? 1 : 0);
  payload.acl_index = m_acl.value();

  VAPI_CALL(req.execute());

  return (wait());
}

template <>
std::string
l3_unbind_cmd::to_string() const
{
  std::ostringstream s;
  s << "l3-acl-unbind:[" << m_direction.to_string()
    << " itf:" << m_itf.to_string() << " acl:" << m_acl.to_string() << "]";

  return (s.str());
}

template <>
rc_t
l3_dump_cmd::issue(connection& con)
{
  m_dump.reset(new msg_t(con.ctx(), std::ref(*this)));

  auto& payload = m_dump->get_request().get_payload();
  payload.sw_if_index = ~0;

  VAPI_CALL(m_dump->execute());

  wait();

  return rc_t::OK;
}

template <>
std::string
l3_dump_cmd::to_string() const
{
  return ("l3-acl-bind-dump");
}

template <>
rc_t
l2_bind_cmd::issue(connection& con)
{
  msg_t req(con.ctx(), std::ref(*this));

  auto& payload = req.get_request().get_payload();
  payload.sw_if_index = m_itf.value();
  payload.is_add = 1;
  payload.acl_index = m_acl.value();

  VAPI_CALL(req.execute());

  return (wait());
}

template <>
std::string
l2_bind_cmd::to_string() const
{
  std::ostringstream s;
  s << "l2-acl-bind:[" << m_direction.to_string()
    << " itf:" << m_itf.to_string() << " acl:" << m_acl.to_string() << "]";

  return (s.str());
}

template <>
rc_t
l2_unbind_cmd::issue(connection& con)
{
  msg_t req(con.ctx(), std::ref(*this));

  auto& payload = req.get_request().get_payload();
  payload.sw_if_index = m_itf.value();
  payload.is_add = 0;
  payload.acl_index = m_acl.value();

  VAPI_CALL(req.execute());

  return (wait());
}

template <>
std::string
l2_unbind_cmd::to_string() const
{
  std::ostringstream s;
  s << "l2-acl-unbind:[" << m_direction.to_string()
    << " itf:" << m_itf.to_string() << " acl:" << m_acl.to_string() << "]";

  return (s.str());
}

template <>
rc_t
l2_dump_cmd::issue(connection& con)
{
  m_dump.reset(new msg_t(con.ctx(), std::ref(*this)));

  auto& payload = m_dump->get_request().get_payload();
  payload.sw_if_index = ~0;

  VAPI_CALL(m_dump->execute());

  wait();

  return rc_t::OK;
}

template <>
std::string
l2_dump_cmd::to_string() const
{
  return ("l2-acl-bind-dump");
}

}; // namespace binding_cmds
}; // namespace ACL
}; // namespace VOM

/*
 * fd.io coding-style-patch-verification: OFF
 *
 * Local Variables:
 * eval: (c-set-style "mozilla")
 * End:
 */
